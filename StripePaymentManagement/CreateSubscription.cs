using System;
using System.Collections.Generic;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Azure.WebJobs;
using Microsoft.Azure.WebJobs.Extensions.Http;
using MySqlConnector;
using Stripe;
using Stripe.Checkout;

namespace Astra.Algo.Payment {
    public static class CreateSubscription {
        [FunctionName ("CreateSubscription")]
        public static async Task<ActionResult> Run ([HttpTrigger (AuthorizationLevel.Anonymous, "get", "post", Route = null)] HttpRequest req) {
            StripeConfiguration.ApiKey = "sk_test_51IMONzIkAX7cDP9rmPb7yrVx0FTUv5YY5N7MGswAIGsSa7PQSh3u0nxvQ6Ut76240f1rl5idATh7qNI3WWp7QkVG00SdpcEvp1"; //Get it from your stripe dashboard
            var userId = req.Query["userId"];
            var connectionString = "Server=astraalgoserv1.mysql.database.azure.com; Port=3306; Database=astraalgo; Uid=AstraAlgo@astraalgoserv1; Pwd=Algoastra2020; SslMode=Preferred;";
            var customerId = string.Empty;

            try
            {
                using (var conn = new MySqlConnection(connectionString)){
                    await conn.OpenAsync();
                    // Try to  get the users stripe customer id from the database
                    string sql = $"SELECT stripe_id FROM users WHERE user_id = '{userId}' LIMIT 1;";
                    MySqlCommand cmd = new MySqlCommand(sql, conn);
                    using (MySqlDataReader rdr = await cmd.ExecuteReaderAsync()){
                        while (rdr.Read()){
                            if(! DBNull.Value.Equals(rdr[0]))
                                customerId = (string) rdr[0];
                        }
                    }

                    // If we cannot get the stripe customer id from the database then we create them as a user in stripe
                    if (string.IsNullOrEmpty(customerId))
                    {
                        var customerOptions = new CustomerCreateOptions {
                            Description = $"User {userId} created",
                        };
                        var customerService = new CustomerService ();
                        var customer = customerService.Create(customerOptions);

                        // Save the users stripe_id
                        sql = $"UPDATE users SET stripe_id = '{customer.Id}' WHERE user_id = '{userId}';";
                        cmd = new MySqlCommand(sql, conn);
                        await cmd.ExecuteNonQueryAsync();
                        customerId = customer.Id;
                    }

                    // If we do not have a customer id then we exit
                    if(string.IsNullOrEmpty(customerId))
                        return new BadRequestObjectResult (customerId);

                    // Create the subscription object with the desired options
                    var options = new SessionCreateOptions {
                        Customer = customerId,
                        PaymentMethodTypes = new List<string> {
                            "card",
                        },
                        LineItems = new List<SessionLineItemOptions> {
                            new SessionLineItemOptions {
                                Quantity = 1,
                                Description = "Monthly Subscription",
                                Price = "price_1IMPuuIkAX7cDP9rjRDRqATi"
                            }
                        },
                        Mode = "subscription",
                        SuccessUrl = "https://localhost:44352/success?session_id={CHECKOUT_SESSION_ID}",
                        CancelUrl = "https://localhost:44352/failed"
                    };

                    // Send the subscription object to stripe to be created
                    var service = new SessionService ();
                    try {
                        var session = await service.CreateAsync(options);
                        return new JsonResult (new { id = session.Id });
                    } catch (StripeException e) {
                        return new BadRequestObjectResult (e.StripeError.Message);
                    }
                }
            }
            catch (Exception ex)
            {
                return new BadRequestObjectResult (ex.Message);
            }
        }
    }
}