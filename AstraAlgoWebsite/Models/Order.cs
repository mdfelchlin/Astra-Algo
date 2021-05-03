
namespace AstraAlgoWebsite.Models
{
    public class Order
    {
        public string OrderId { get; set; }
        public string Company { get; set; }
        public string Ticker { get; set; }
        public int Shares { get; set; }
        public double CostBasis { get; set; }
        public double Amount { get; set; }
    }
}
