using System;
using System.Net.Http;
using System.Threading.Tasks;
using AstraAlgoWebsite.Services;
using Blazor.Fluxor;
using Microsoft.AspNetCore.Components.WebAssembly.Hosting;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using Radzen;

namespace AstraAlgoWebsite
{
    public class Program
    {
        public static async Task Main(string[] args)
        {
            var builder = WebAssemblyHostBuilder.CreateDefault(args);
            builder.RootComponents.Add<App>("#app");

            builder.Services.AddScoped<IAccountService, AccountService>();

            builder.Services.AddScoped(sp => new HttpClient { BaseAddress = new Uri("http://localhost:7072") });

            builder.Services.AddOidcAuthentication(options =>
            {
                builder.Configuration.Bind("Auth0", options.ProviderOptions);
                options.ProviderOptions.ResponseType = "code";
            });

            // Add fluxor to the project
            builder.Services.AddFluxor(options => options.UseDependencyInjection(typeof(Program).Assembly));

            // Radzen Component imports
            builder.Services.AddScoped<DialogService>();
            builder.Services.AddScoped<NotificationService>();
            builder.Services.AddScoped<TooltipService>();
            builder.Services.AddScoped<ContextMenuService>();

            await builder.Build().RunAsync();
        }
    }
}
