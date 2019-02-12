rm(list = ls())

getwd()

library(DBI)
library(RSQLite)

db_name <- file.path('data', 'advfn.sqlite')

conn <- dbConnect(SQLite(), db_name)
dbDisconnect(conn)

library(xml2)

alphabet_capital <- c('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q',
                      'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z')


# Collect equity names and symbols for all equities on the New York Stock Exchange
url_prefix_nyse <- "http://www.advfn.com/nyse/newyorkstockexchange.asp?companies="
url_suffix_nyse <- ''
matrix_equities_nyse <- matrix(nrow = 0, ncol = 2)

for (i in 1:length(alphabet_capital)) {
  url_suffix_nyse <- alphabet_capital[i]
  url_current_nyse <- paste(url_prefix_nyse, url_suffix_nyse, sep='')
  current_page_nyse <- read_html(url_current_nyse)
  current_equities_nyse <- xml_find_all(current_page_nyse, "//tr[@class='ts0' or @class='ts1']//text()")
  list_equities_nyse <- as_list(current_equities_nyse)
  matrix_equities_nyse <- rbind(matrix_equities_nyse, matrix(list_equities_nyse, nrow = length(list_equities_nyse)/2, ncol = 2, byrow = TRUE))
  print(url_current_nyse)
}

# Collect equity names and symbols for all equities on the Nasdaq
url_prefix_nasdaq <- "http://www.advfn.com/nasdaq/nasdaq.asp?companies="
url_suffix_nasdaq <- ''
matrix_equities_nasdaq <- matrix(nrow = 0, ncol = 2)

for (i in 1:length(alphabet_capital)) {
  url_suffix_nasdaq <- alphabet_capital[i]
  url_current_nasdaq <- paste(url_prefix_nasdaq, url_suffix_nasdaq, sep='')
  current_page_nasdaq <- read_html(url_current_nasdaq)
  current_equities_nasdaq <- xml_find_all(current_page_nasdaq, "//tr[@class='ts0' or @class='ts1']//text()")
  list_equities_nasdaq <- as_list(current_equities_nasdaq)
  matrix_equities_nasdaq <- rbind(matrix_equities_nasdaq, matrix(list_equities_nasdaq, nrow = length(list_equities_nasdaq)/2, ncol = 2, byrow = TRUE))
  print(url_current_nasdaq)
}