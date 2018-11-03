import subprocess

testing_cases=["currency_cli.py --amount 10 --input_currency CZK --output_currency USD",
"currency_cli.py --amount 10 --input_currency CZK --output_currency CAD",
"currency_cli.py --amount 10 --input_currency CZK --output_currency EUR",
"currency_cli.py --amount 10 --input_currency CZK --output_currency AUD",
"currency_cli.py --amount 10 --input_currency CZK --output_currency BGN",
"currency_cli.py --amount 10 --input_currency CZK --output_currency BRL",
"currency_cli.py --amount 10 --input_currency CZK --output_currency CHF",
"currency_cli.py --amount 10 --input_currency CZK --output_currency CNY",
"currency_cli.py --amount 10 --input_currency CZK --output_currency CZK",
"currency_cli.py --amount 10 --input_currency CZK --output_currency DKK",
"currency_cli.py --amount 10 --input_currency CZK --output_currency GBP",
"currency_cli.py --amount 10 --input_currency CZK --output_currency HKD",
"currency_cli.py --amount 10 --input_currency CZK --output_currency HRK",
"currency_cli.py --amount 10 --input_currency CZK --output_currency HUF",
"currency_cli.py --amount 10 --input_currency CZK --output_currency IDR",
"currency_cli.py --amount 10 --input_currency CZK --output_currency ILS",
"currency_cli.py --amount 10 --input_currency CZK --output_currency INR",
"currency_cli.py --amount 10 --input_currency CZK --output_currency ISK",
"currency_cli.py --amount 10 --input_currency CZK --output_currency JPY",
"currency_cli.py --amount 10 --input_currency CZK --output_currency KRW",
"currency_cli.py --amount 10 --input_currency CZK --output_currency MXN",
"currency_cli.py --amount 10 --input_currency CZK --output_currency MYR",
"currency_cli.py --amount 10 --input_currency CZK --output_currency NOK",
"currency_cli.py --amount 10 --input_currency CZK --output_currency NZD",
"currency_cli.py --amount 10 --input_currency CZK --output_currency PHP",
"currency_cli.py --amount 10 --input_currency CZK --output_currency PLN",
"currency_cli.py --amount 10 --input_currency CZK --output_currency RON",
"currency_cli.py --amount 10 --input_currency CZK --output_currency RUB",
"currency_cli.py --amount 10 --input_currency CZK --output_currency SEK",
"currency_cli.py --amount 10 --input_currency CZK --output_currency SGD",
"currency_cli.py --amount 10 --input_currency CZK --output_currency THB",
"currency_cli.py --amount 10 --input_currency CZK --output_currency TRY",
"currency_cli.py --amount 10 --input_currency CZK --output_currency ZAR"
]
for test_case in testing_cases:
    subprocess.Popen(test_case, shell=True)
    input('continue')
    