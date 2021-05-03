using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace AstraAlgoWebsite.Models
{
    public class Position
    {
        //public int shortQuantity { get; set; }
        public double averagePrice { get; set; }
        public double currentDayProfitLoss { get; set; }
        public double currentDayProfitLossPercentage { get; set; }
        public double longQuantity { get; set; }
        //public double settledLongQuantity { get; set; }
        //public int settledShortQuantity { get; set; }
        
        
        public Instrument instrument { get; set; }
        public double marketValue { get; set; }
        //public int maintenanceRequirement { get; set; }
    }
}
