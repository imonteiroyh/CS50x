-- Keep a log of any SQL queries you execute as you solve the mystery.

-- Investigando a cena de crime, o roubo foi realizado na padaria às 10:15am
SELECT *
FROM crime_scene_reports
WHERE year = 2021 AND month = 7 AND day = 28 AND street = 'Humphrey Street';

-- Investigando depoimentos
-- Ruth: O ladrão fugiu dentro de 10 minutos do local após o roubo
-- Eugene: Reconheceu o ladrão, estava andando na ATM na Leggett Street e viu o ladrão retirando dinheiro
-- Raymond: O ladrão ligou para alguém que falou por menos de um minuto depois de fugir, disse que pegaria o voo mais cedo para fora de Fiftyville no dia seguinte e pediu para a outra pessoa na linha comprar o voo
SELECT name, transcript
FROM interviews
WHERE year = 2021 AND month = 7 AND day = 28;

-- Investigando os suspeitos que entraram antes da hora do crime e saíram depois
SELECT license_plate
    FROM bakery_security_logs
    WHERE license_plate IN
        (SELECT license_plate
        FROM bakery_security_logs
        WHERE year = 2021 AND month = 7 AND day = 28 AND
            (activity = 'entrance' AND hour <= 10 AND minute <= 15)
        ORDER BY license_plate)
        AND year = 2021 AND month = 7 AND day = 28 AND
            (activity = 'exit' AND hour = 10 AND minute <= 25);

-- Encontrando as informações dos suspeitos com base nas placas (Vanessa, Luca)
SELECT *
FROM people
WHERE license_plate IN
    (SELECT license_plate
    FROM bakery_security_logs
    WHERE license_plate IN
        (SELECT license_plate
        FROM bakery_security_logs
        WHERE year = 2021 AND month = 7 AND day = 28 AND
            (activity = 'entrance' AND hour <= 10 AND minute <= 15)
        ORDER BY license_plate)
        AND year = 2021 AND month = 7 AND day = 28 AND
            (activity = 'exit' AND hour = 10 AND minute <= 25));

-- Investigando as ligações realizadas nesse dia pelos dois suspeitos, apenas uma duração de 1 minuto, de Luca
SELECT *
FROM phone_calls
WHERE year = 2021 AND month = 7 AND day = 28 AND
    (caller IN
        (SELECT phone_number
        FROM people
        WHERE license_plate IN
            (SELECT license_plate
            FROM bakery_security_logs
            WHERE license_plate IN
                (SELECT license_plate
                FROM bakery_security_logs
                WHERE year = 2021 AND month = 7 AND day = 28 AND
                    (activity = 'entrance' AND hour <= 10 AND minute <= 15)
                ORDER BY license_plate)
                AND year = 2021 AND month = 7 AND day = 28 AND
                    (activity = 'exit' AND hour = 10 AND minute <= 25)))
    OR receiver IN
        (SELECT phone_number
        FROM people
        WHERE license_plate IN
            (SELECT license_plate
            FROM bakery_security_logs
            WHERE license_plate IN
                (SELECT license_plate
                FROM bakery_security_logs
                WHERE year = 2021 AND month = 7 AND day = 28 AND
                    (activity = 'entrance' AND hour <= 10 AND minute <= 15)
                ORDER BY license_plate)
                AND year = 2021 AND month = 7 AND day = 28 AND
                    (activity = 'exit' AND hour = 10 AND minute <= 25))));

-- Verificando se Luca retirou dinheiro antes, como dito pela testemunha. Sim, retirou
SELECT *
FROM atm_transactions
WHERE year = 2021 AND month = 7 AND day = 28 AND atm_location = 'Leggett Street' AND transaction_type = 'withdraw' AND account_number IN
    (SELECT account_number
    FROM bank_accounts
    WHERE person_id = '467400');

-- 
SELECT *
FROM flights
WHERE origin_airport_id =
    (SELECT id
    FROM airports
    WHERE city = 'Fiftyville')
AND year = 2021 AND month = 7 AND day = 29
ORDER BY hour, minute;