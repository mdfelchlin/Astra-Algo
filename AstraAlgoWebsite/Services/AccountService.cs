using AstraAlgoWebsite.Models;
using Microsoft.AspNetCore.Components;
using Microsoft.AspNetCore.Components.Authorization;
using Newtonsoft.Json;
using System.Collections.Generic;
using System.Linq;
using System.Net.Http;
using System.Net.Http.Json;
using System.Threading.Tasks;

namespace AstraAlgoWebsite.Services
{
    public class AccountService : IAccountService
    {
        private string _userId = string.Empty;
        private readonly AuthenticationStateProvider _authenticationState;
        private readonly HttpClient _httpClient;
        private readonly NavigationManager _navigationManager;

        public AccountService(
            AuthenticationStateProvider authenticationState,
            HttpClient httpClient,
            NavigationManager navigationManager)
        {
            _authenticationState = authenticationState;
            _httpClient = httpClient;
            _navigationManager = navigationManager;
        }

        public async Task<Account> GetAccountAsync()
        {
            _userId = await GetUserIdAsync();
            _httpClient.DefaultRequestHeaders.Clear();
            _httpClient.DefaultRequestHeaders.Add("user_id", _userId);
            var result = await _httpClient.GetAsync(FunctionURIs.GetAccountInformation);
            if (result.IsSuccessStatusCode)
                return await result.Content.ReadFromJsonAsync<Account>();
            return new Account();
        }

        public async Task<SecuritiesAccount> GetTDAccountAsync()
        {
            _userId = await GetUserIdAsync();
            _httpClient.DefaultRequestHeaders.Clear();
            _httpClient.DefaultRequestHeaders.Add("user_id", _userId);
            var result = await _httpClient.GetAsync(FunctionURIs.GetTDAccountInformation);
            if (result.IsSuccessStatusCode)
                return await result.Content.ReadFromJsonAsync<SecuritiesAccount>();
            return null;
        }

        public async Task<Account> SaveUsersCredentialsAsync()
        {
            var code = _navigationManager.Uri.Split(ApplicationConstants.UrlCodeParameter)[1];
            _userId = await GetUserIdAsync();
            _httpClient.DefaultRequestHeaders.Clear();
            _httpClient.DefaultRequestHeaders.Add("user_id", _userId);
            _httpClient.DefaultRequestHeaders.Add("code", code);
            var result = await _httpClient.GetAsync(FunctionURIs.SaveUserCredentials);
            if (result.IsSuccessStatusCode)
                return await result.Content.ReadFromJsonAsync<Account>();
            return new Account();
        }

        public async Task SaveUserAccountInformationAsync(Account account)
        {
            _userId = await GetUserIdAsync();
            _httpClient.DefaultRequestHeaders.Clear();
            _httpClient.DefaultRequestHeaders.Add("user_id", _userId);
            await _httpClient.PostAsJsonAsync(FunctionURIs.UpdateUserAccountInformation, account);
        }

        public async Task<Account> SaveUsersDiscordAccountAsync()
        {
            var code = _navigationManager.Uri.Split(ApplicationConstants.UrlCodeParameter)[1];
            _userId = await GetUserIdAsync();
            _httpClient.DefaultRequestHeaders.Clear();
            _httpClient.DefaultRequestHeaders.Add("user_id", _userId);
            _httpClient.DefaultRequestHeaders.Add("code", code);
            var result = await _httpClient.GetAsync(FunctionURIs.UpdateUserAfterDiscordLogin);
            if (result.IsSuccessStatusCode)
                return await result.Content.ReadFromJsonAsync<Account>();
            return new Account();
        }

        public async Task<Account> RemoveConnectedAccountAsync(ConnectedAccounts account)
        {
            _userId = await GetUserIdAsync();
            _httpClient.DefaultRequestHeaders.Clear();
            _httpClient.DefaultRequestHeaders.Add("user_id", _userId);
            var accountToRemove = string.Empty;
            switch (account)
            {
                case ConnectedAccounts.Discord:
                    accountToRemove = "Discord";
                    break;
                case ConnectedAccounts.TDA:
                    accountToRemove = "TDA";
                    break;
            }
            _httpClient.DefaultRequestHeaders.Add("account", accountToRemove);
            var result = await _httpClient.GetAsync(FunctionURIs.RemoveConnectedAccount);
            if (result.IsSuccessStatusCode)
                return await result.Content.ReadFromJsonAsync<Account>();
            return new Account();
        }

        public async Task<Dictionary<string, Stock>> GetInstrumentsAsync(string symbols)
        {
            _userId = await GetUserIdAsync();
            _httpClient.DefaultRequestHeaders.Clear();
            _httpClient.DefaultRequestHeaders.Add("user_id", _userId);
            _httpClient.DefaultRequestHeaders.Add("symbols", symbols);
            var result = await _httpClient.GetAsync(FunctionURIs.GetInstruments);
            if (result.IsSuccessStatusCode)
            {
                var jsonString = await result.Content.ReadAsStringAsync();
                return JsonConvert.DeserializeObject<Dictionary<string, Stock>>(jsonString);
            }
            return null;
        }

        public async Task ActivateSubscriptionAsync()
        {
            _userId = await GetUserIdAsync();
            await _httpClient.GetAsync(FunctionURIs.ActivateSubscription + $"&userId={_userId}");
        }

        public async Task<bool> CancelSubscriptionAsync()
        {
            _userId = await GetUserIdAsync();
            var result = await _httpClient.GetAsync(FunctionURIs.CancelSubscription + $"&userId={_userId}");
            if (result.IsSuccessStatusCode) return true;
            else return false;
        }

        public async Task <string> GetUserIdAsync()
        {
            var claim = await _authenticationState.GetAuthenticationStateAsync();
            var userClaim = claim.User.Claims.FirstOrDefault(x => x.Type == "sub");
            var userId = userClaim.Value.Split("|");
            return userId[1];
        }
    }
}
