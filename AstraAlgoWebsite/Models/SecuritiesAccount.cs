using Newtonsoft.Json;
using System.Collections.Generic;

namespace AstraAlgoWebsite.Models
{

    public class SecuritiesAccount
    {
        public string type { get; set; }
        public string accountId { get; set; }
        public int roundTrips { get; set; }
        public bool isDayTrader { get; set; }
        public bool isClosingOnlyRestricted { get; set; }
        
        public List<Position> positions { get; set; }
        public InitialBalances initialBalances { get; set; }
        public CurrentBalances currentBalances { get; set; }
        public ProjectedBalances projectedBalances { get; set; }
    }
}
