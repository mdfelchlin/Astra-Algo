using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace AstraAlgoWebsite.Store
{
    public class StartPaymentSuccessAction
    {
        public string token { get; private set; }

        public StartPaymentSuccessAction(string token)
        {
            this.token = token;
        }
    }
}
