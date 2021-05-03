namespace AstraAlgoWebsite.Services
{
    public static class ApplicationConstants
    {
        public static readonly string RedirectUri = "https://localhost:44352/account";
        public static readonly string TDARedirectUri = "https://localhost:44352/account/td";
        public static readonly string DiscordRedirectUri = "https://localhost:44352/account/discord/";
        public static readonly string ApiKey = "NYDHGTAWWLQ47ZOO9OTDLVSTOGUVPYQX@AMER.OAUTHAP";
        public static readonly string UrlCodeParameter = "code=";
        public static readonly string DiscordRoute = "discord";
        public static readonly string TdRoute = "td";
        public static string TDALoginUrl => 
            "https://auth.tdameritrade.com/auth?"
            + "response_type=code" 
            + "&client_id=" + ApiKey 
            + "&redirect_uri=" + TDARedirectUri;

        private static readonly string DiscordClientId = "809190579610058823";
        public static string DiscordLoginUrl =>
            "https://discordapp.com/api/oauth2/authorize?" 
            + "client_id=" + DiscordClientId
            + "&scope=identify"
            + "&response_type=code"
            + "&redirect_uri=" + DiscordRedirectUri;
    }
}
