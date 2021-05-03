using System;

namespace AstraAlgoWebsite.Models
{
    public class Account
    {
        public string lastname { get; set; }
        public string firstname { get; set; }
        public string email { get; set; }
        public string phoneNumber { get; set; }
        public string discordUsername { get; set; }
        public string tdAmeritradeUsername { get; set; }
        public int buyTextMessage { get; set; }
        public int buyEmail { get; set; }
        public int buyDiscord { get; set; }
        public int sellTextMessage { get; set; }
        public int sellEmail { get; set; }
        public int sellDiscord { get; set; }
        public int subscriptionActive { get; set; }

        public override bool Equals(object account)
        {
            return Equals(account as Account);
        }

        public bool Equals(Account other)
        {
            return other.firstname == this.firstname &&
                   other.lastname == this.lastname &&
                   other.email == this.email &&
                   other.phoneNumber == this.phoneNumber &&
                   other.buyEmail == this.buyEmail &&
                   other.sellEmail == this.sellEmail &&
                   other.buyTextMessage == this.buyTextMessage &&
                   other.sellTextMessage == this.sellTextMessage &&
                   other.buyDiscord == this.buyDiscord &&
                   other.sellDiscord == this.sellDiscord;
        }

        public Account DeepCopy() => new Account
        {
            firstname = this.firstname,
            lastname = this.lastname,
            email = this.email,
            phoneNumber = this.phoneNumber,
            buyEmail = this.buyEmail,
            sellEmail = this.sellEmail,
            buyTextMessage = this.buyTextMessage,
            sellTextMessage = this.sellTextMessage,
            buyDiscord = this.buyDiscord,
            sellDiscord = this.sellDiscord
        };

        public override int GetHashCode()
        {
            return 1;
        }
    }
}
