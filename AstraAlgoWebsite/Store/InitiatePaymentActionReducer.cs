using Blazor.Fluxor;

namespace AstraAlgoWebsite.Store
{
    public class InitiatePaymentActionReducer : Reducer<PaymentState, InitiatePaymentAction>
    {
        public override PaymentState Reduce(PaymentState state, InitiatePaymentAction action)
        {
            return new PaymentState(
                isLoading: true,
                errorMessage: null,
                token: null
                );
        }
    }
}
