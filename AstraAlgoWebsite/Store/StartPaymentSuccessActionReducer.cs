using Blazor.Fluxor;

namespace AstraAlgoWebsite.Store
{
    public class StartPaymentSuccessActionReducer : Reducer<PaymentState, StartPaymentSuccessAction>
    {
        public override PaymentState Reduce(PaymentState state, StartPaymentSuccessAction action)
        {
            return new PaymentState(
                isLoading: false,
                errorMessage: null,
                token: action.token
                );
        }
    }
}
