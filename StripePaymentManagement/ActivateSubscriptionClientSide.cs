using System;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Azure.WebJobs;
using Microsoft.Azure.WebJobs.Extensions.Http;
using Microsoft.AspNetCore.Http;
using Microsoft.Extensions.Logging;
using MySqlConnector;

namespace Company.Function
{
    public static class ActivateSubscriptionClientSide
    {
        [FunctionName("ActivateSubscriptionClientSide")]
        public static async Task<IActionResult> Run(
            [HttpTrigger(AuthorizationLevel.Anonymous, "get", "post", Route = null)] HttpRequest req,
            ILogger log)
        {
            var userId = req.Query["userId"];
            var connectionString = "Server=astraalgoserv1.mysql.database.azure.com; Port=3306; Database=astraalgo; Uid=AstraAlgo@astraalgoserv1; Pwd=Algoastra2020; SslMode=Preferred;";

            try
            {
                using (var conn = new MySqlConnection(connectionString)){
                    await conn.OpenAsync();
                    var sql = $"UPDATE users SET subscription_active = 1 WHERE user_id = '{userId}'";
                    var cmd = new MySqlCommand(sql, conn);
                    await cmd.ExecuteNonQueryAsync();
                }
            }
            catch (Exception ex)
            {
                return new BadRequestObjectResult (ex.Message);
            }

            return new OkObjectResult("Subscription Activated");
        }
    }
}
