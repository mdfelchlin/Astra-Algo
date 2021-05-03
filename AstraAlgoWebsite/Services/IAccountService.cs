using AstraAlgoWebsite.Models;
using System.Collections.Generic;
using System.Net.Http;
using System.Threading.Tasks;

namespace AstraAlgoWebsite.Services
{
    public interface IAccountService
    {
        /// <summary>
        /// Method to get the users data from out database to display on the account page
        /// </summary>
        Task<Account> GetAccountAsync();

        /// <summary>
        /// Method to get the users TD Ameritrade account information
        /// </summary>
        Task<SecuritiesAccount> GetTDAccountAsync();

        /// <summary>
        /// Once the user logs into their TD Ameritrade Account save it in the database
        /// </summary>
        Task<Account> SaveUsersCredentialsAsync();

        /// <summary>
        /// Save the users account information in the database
        /// </summary>
        /// <returns></returns>
        Task SaveUserAccountInformationAsync(Account account);

        /// <summary>
        /// Once the user logins in to their discord account parse the code from the URL and save them in the database
        /// </summary>
        Task<Account> SaveUsersDiscordAccountAsync();

        /// <summary>
        /// Removes the desired connected account for the user in our database
        /// </summary>
        Task<Account> RemoveConnectedAccountAsync(ConnectedAccounts account);

        Task<Dictionary<string,Stock>> GetInstrumentsAsync(string symbols);

        /// <summary>
        /// Get the users id for commands
        /// </summary>
        Task<string> GetUserIdAsync();

        /// <summary>
        /// Cancel the users subscription
        /// </summary>
        Task<bool> CancelSubscriptionAsync();

        /// <summary>
        /// When the user completes the payment process we need to mark in our database that their
        /// subscription is active
        /// </summary>
        Task ActivateSubscriptionAsync();
    }
}
