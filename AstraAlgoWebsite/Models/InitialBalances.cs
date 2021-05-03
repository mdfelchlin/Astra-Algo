
namespace AstraAlgoWebsite.Models
{
    public class InitialBalances
    {
        public decimal accruedInterest { get; set; }
        public decimal cashAvailableForTrading { get; set; }
        public decimal cashAvailableForWithdrawal { get; set; }
        public decimal cashBalance { get; set; }
        public decimal bondValue { get; set; }
        public decimal cashReceipts { get; set; }
        public decimal liquidationValue { get; set; }
        public decimal longOptionMarketValue { get; set; }
        public decimal longStockValue { get; set; }
        public decimal moneyMarketFund { get; set; }
        public decimal mutualFundValue { get; set; }
        public decimal shortOptionMarketValue { get; set; }
        public decimal shortStockValue { get; set; }
        public bool isInCall { get; set; }
        public decimal unsettledCash { get; set; }
        public decimal cashDebitCallValue { get; set; }
        public decimal pendingDeposits { get; set; }
        public decimal accountValue { get; set; }
    }
}
