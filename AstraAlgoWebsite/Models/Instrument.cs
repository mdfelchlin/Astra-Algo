using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace AstraAlgoWebsite.Models
{
    public class Instrument
    {
        public string assetType { get; set; }
        public string cusip { get; set; }
        public string symbol { get; set; }
        public string description { get; set; }
        public string type { get; set; }
    }
}
