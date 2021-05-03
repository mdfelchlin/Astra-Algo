using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace AstraAlgoWebsite.Store
{
    public class StartPaymentFailedAction
    {
        public string error { get; private set; }

        public StartPaymentFailedAction(string error)
        {
            this.error = error;
        }
    }
}
