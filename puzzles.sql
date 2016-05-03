-- Count of unique beers added to ftiso in past month
SELECT beer_id, COUNT(beer_id) AS beer_count
FROM ftiso
WHERE type = "ft"
  AND DATE(created) > (NOW() - INTERVAL 30 DAY)
  AND beer_count > 1
GROUP BY beer_id;

-- Ranked list of beers with more than one @WISHLIST_TYPE add in past @NUM_DAYS
SET @NUM_DAYS = 100;
SET @WISHLIST_TYPE = "ft";

SELECT DISTINCT ftiso.beer_id, wishlist.beer_count
FROM ftiso
LEFT OUTER JOIN (
  SELECT beer_id, COUNT(beer_id) AS beer_count
  FROM ftiso
  WHERE type = @WISHLIST_TYPE
    AND DATE(created) > (NOW() - INTERVAL @NUM_DAYS DAY)
  GROUP BY beer_id
) AS wishlist
ON wishlist.beer_id = ftiso.beer_id
WHERE wishlist.beer_count > 1
ORDER BY wishlist.beer_count DESC;

-- Count of user registrations by

-- Day
SELECT DATE(created), COUNT(id)
FROM users
-- WHERE status = 0
  -- AND member_type < 3
GROUP BY DATE(created)
ORDER BY DATE(created) DESC;

-- Day of week
SELECT WEEKDAY(created), COUNT(id)
FROM users
GROUP BY WEEKDAY(created)
ORDER BY WEEKDAY(created) DESC;

-- Hour
SELECT HOUR(created), COUNT(id)
FROM users
GROUP BY HOUR(created)
ORDER BY HOUR(created) DESC;

/* Generates list of average beers a user includes in a trade,
grouped by state */
SELECT users.state, AVG(user_beers.beer_count)
FROM trades
-- generates count of beers per trade, grouped by user
INNER JOIN (
    SELECT trade_items.user_id AS user_id, trade_items.trade_id, SUM(trade_items.quantity) AS beer_count
    FROM trade_items
    GROUP BY trade_items.user_id, trade_items.trade_id
    ) AS user_beers
ON trades.id = user_beers.trade_id
INNER JOIN users
ON users.id = user_beers.user_id
WHERE trades.user1_status = 2
AND trades.user2_status = 2
GROUP BY users.state;

/* Return the count of each user's most messaged person */
SELECT sender_id, receiver_id, MAX(msgs)
FROM (
  -- Returns the count of user/recipient messages
  SELECT sender_id, receiver_id, COUNT(*) AS msgs
  FROM messages
  GROUP BY sender_id, receiver_id
) AS msg_count
GROUP BY sender_id;


/* Returns average count of unique wishlist items for churned users */
SELECT AVG(wishlist.cnt)
FROM users
LEFT OUTER JOIN (
  -- wishlist count
  SELECT user_id, COUNT(id) AS cnt
	FROM ftiso
	GROUP BY user_id
    ) AS wishlist
ON users.id = wishlist.user_id
WHERE (users.id, users.id) NOT IN (
  --non churn users, NOT IN statement implies OR syntax
  SELECT user1_id, user2_id
	FROM trades
	WHERE created > DATE('2015-09-30') - INTERVAL 90 DAY
	ORDER BY `trades`.`created` DESC
)
