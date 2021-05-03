using System;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Azure.WebJobs;
using Microsoft.Azure.WebJobs.Extensions.Http;
using MySqlConnector;
using Stripe;

namespace Astra.Algo.Payment {
    public static class CancelSubscription {
        [FunctionName ("CancelSubscription")]
        public static async Task<IActionResult> Run (
            [HttpTrigger (AuthorizationLevel.Anonymous, "get", "post", Route = null)] HttpRequest req) 
        {
            StripeConfiguration.ApiKey = "sk_test_51IMONzIkAX7cDP9rmPb7yrVx0FTUv5YY5N7MGswAIGsSa7PQSh3u0nxvQ6Ut76240f1rl5idATh7qNI3WWp7QkVG00SdpcEvp1"; //Get it from your stripe dashboard
            var userId = req.Query["userId"];
            var connectionString = "Server=astraalgoserv1.mysql.database.azure.com; Port=3306; Database=astraalgo; Uid=AstraAlgo@astraalgoserv1; Pwd=Algoastra2020; SslMode=Preferred;";
            var customerId = string.Empty;
            
            try
            {
                using (var conn = new MySqlConnection(connectionString)){
                    await conn.OpenAsync();
                    string sql = $"SELECT stripe_id FROM users WHERE user_id = '{userId}' LIMIT 1";
                    MySqlCommand cmd = new MySqlCommand(sql, conn);
                    using (MySqlDataReader rdr = cmd.ExecuteReader()){
                        while (rdr.Read())
                            customerId = (string) rdr[0];
                    }

                    var options = new SubscriptionListOptions
                    {
                        Customer = customerId
                    };

                    var service = new SubscriptionService();
                    StripeList<Subscription> subscriptions = await service.ListAsync(options);

                    var subscription = subscriptions.FirstOrDefault();
                    // Cancel subscription
                    if(subscription != null){
                        await service.CancelAsync(subscription.Id, null);
                        sql = $"UPDATE users SET subscription_active = 0 WHERE user_id = '{userId}';";
                        cmd = new MySqlCommand(sql, conn);
                        await cmd.ExecuteNonQueryAsync();

                        return new OkObjectResult ("Canceled Subscription");
                    }
                    else{
                        return new BadRequestObjectResult("Subscription not found");
                    }
                }
            }
            catch (Exception ex)
            {
                return new BadRequestObjectResult(ex.ToString());
            }
        }
    }
}