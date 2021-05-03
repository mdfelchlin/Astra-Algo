namespace AstraAlgoWebsite.Services
{
    public static class FunctionURIs
    {
        public static readonly string SaveUserCredentials = "https://tdameritradeauthentication.azurewebsites.net/api/UpdateUserAfterTDALogin?code=RVuK05I0jLzWEqXGjW97C9zRak1wFxwZAhmq4YiUVWpYBbJjN0epcw==";
        public static readonly string GetAccountInformation = "https://tdameritradeauthentication.azurewebsites.net/api/GetAccountInformation?code=sr5j47ZYT5M2Uo7NGDZMuGpQ6F4K9o5nU9bhHHUXe41lgneeIBapjw==";
        public static readonly string UpdateUserAccountInformation = "https://tdameritradeauthentication.azurewebsites.net/api/UpdateUser?code=Hn3ZypWqlQT1OffBYcoHObaRssQpAbCh6X8xj4TSt80fLa6TEk1dNg==";
        public static readonly string GetTDAccountInformation = "https://tdameritradeauthentication.azurewebsites.net/api/GetDashboardData?code=5SqHX3gGfVORgVqlqDGUC3V4oCo9txOoavxSkaB0khEoPNyhBrF8mA==";
        public static readonly string UpdateUserAfterDiscordLogin = "https://tdameritradeauthentication.azurewebsites.net/api/UpdateUserAfterDiscordLogin?code=4vdYT4W/eLSUXPwab2c5P2TLv4BuAcoAaAFHsSnlcwx/frXs1N7WLg==";
        public static readonly string GetInstruments = "https://tdameritradeauthentication.azurewebsites.net/api/GetInstrumentData?code=9K8OhOP9aVamCztcTvDLuf35DCm0KHm7fuG3alhgq4O5CRiIY5N2WQ==";
        public static readonly string RemoveConnectedAccount = "https://tdameritradeauthentication.azurewebsites.net/api/RemoveConnectedAccounts?code=sYbXLdKeS/59uzNfKy7kqSuv2xE5sa792siWAle4kTqEpdglQ6wF3A==";
        public static readonly string CancelSubscription = "https://stripepaymentmanagement.azurewebsites.net/api/CancelSubscription?code=fbvPj6uABSpFb0lrM5d0REO9kNddO5s0FD0aEH2JGkO1JxziNoHVcw==";
        public static readonly string ActivateSubscription = "https://stripepaymentmanagement.azurewebsites.net/api/ActivateSubscriptionClientSide?";
    }
}
