using Newtonsoft.Json;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace AstraAlgoWebsite.Models
{
    public class Stock
    {
        [JsonProperty("symbol")]
        public string symbol { get; set; }

        [JsonProperty("assetType")]
        public string assetType { get; set; }

        [JsonProperty("openPrice")]
        public double openPrice { get; set; }

        [JsonProperty("highPrice")]
        public double highPrice { get; set; }

        [JsonProperty("lowPrice")]
        public double lowPrice { get; set; }

        [JsonProperty("assetMainType")]
        public string assetMainType { get; set; }

        [JsonProperty("cusip")]
        public string cusip { get; set; }

        [JsonProperty("description")]
        public string description { get; set; }

        [JsonProperty("bidPrice")]
        public double bidPrice { get; set; }

        [JsonProperty("bidSize")]
        public int bidSize { get; set; }

        [JsonProperty("bidId")]
        public string bidId { get; set; }

        [JsonProperty("askPrice")]
        public double askPrice { get; set; }

        [JsonProperty("askSize")]
        public int askSize { get; set; }

        [JsonProperty("askId")]
        public string askId { get; set; }

        [JsonProperty("lastPrice")]
        public double lastPrice { get; set; }

        [JsonProperty("lastSize")]
        public int lastSize { get; set; }

        [JsonProperty("lastId")]
        public string lastId { get; set; }

        [JsonProperty("bidTick")]
        public string bidTick { get; set; }

        [JsonProperty("closePrice")]
        public double closePrice { get; set; }

        [JsonProperty("netChange")]
        public double netChange { get; set; }

        [JsonProperty("totalVolume")]
        public int totalVolume { get; set; }

        [JsonProperty("quoteTimeInLong")]
        public long quoteTimeInLong { get; set; }

        [JsonProperty("tradeTimeInLong")]
        public long tradeTimeInLong { get; set; }

        [JsonProperty("mark")]
        public double mark { get; set; }

        [JsonProperty("exchange")]
        public string exchange { get; set; }

        [JsonProperty("exchangeName")]
        public string exchangeName { get; set; }

        [JsonProperty("marginable")]
        public bool marginable { get; set; }

        [JsonProperty("shortable")]
        public bool shortable { get; set; }

        [JsonProperty("votalility")]
        public double volatility { get; set; }

        [JsonProperty("digits")]
        public int digits { get; set; }

        [JsonProperty("52WkHigh")]
        public double _52WkHigh { get; set; }

        [JsonProperty("52WkLow")]
        public double _52WkLow { get; set; }



        [JsonProperty("regularMarketLastSize")]
        public int regularMarketLastSize { get; set; }

        [JsonProperty("regularMarketNetChange")]
        public double regularMarketNetChange { get; set; }

        [JsonProperty("regularMarketTradeTimeInLong")]
        public long regularMarketTradeTimeInLong { get; set; }

        [JsonProperty("netPercentChangeInDouble")]
        public double netPercentChangeInDouble { get; set; }

        [JsonProperty("markChangeInDouble")]
        public double markChangeInDouble { get; set; }

        [JsonProperty("markPercentChangeInDouble")]
        public double markPercentChangeInDouble { get; set; }

        [JsonProperty("regularMarketPercentChangeInDouble")]
        public double regularMarketPercentChangeInDouble { get; set; }

        [JsonProperty("delayed")]
        public bool delayed { get; set; }

    }
}
