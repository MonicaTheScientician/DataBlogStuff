suppressPackageStartupMessages(library(tidyverse))
suppressPackageStartupMessages(library(lm.beta))
suppressPackageStartupMessages(library(dplyr))
suppressPackageStartupMessages(library("olsrr"))

vgsales <- read_csv('vgsales.csv')

colSums(vgsales == 'N/A')

vgsales <- vgsales[!(vgsales$Year == 'N/A' | vgsales$Publisher == 'N/A'),]
colSums(vgsales == 'N/A')

str(vgsales)

#Global Sales
ggplot(
  head(vgsales, 11),
  aes(x=Global_Sales,
      y=reorder(Name, Global_Sales),
      fill=Platform)) +
  geom_bar(stat="identity") +
  labs(y="Name", x="Global Sales (in million USD)") +
  ggtitle("Top 11 Games in Global Sales")


#NA Sales


NASales <- vgsales %>%
  arrange(desc(NA_Sales))

ggplot(
  head(NASales, 11),
  aes(
    x=NA_Sales,
    y=reorder(Name, NA_Sales),
    fill=Platform)) +
  geom_bar(stat="identity") +
  labs(y="Name",x="North American Sales (in million USD)") +
  ggtitle("Top 11 Games in North American Sales")

#Japan Sales

JPSales <- vgsales %>%
  arrange(desc(JP_Sales))

ggplot(
  head(JPSales, 11),
  aes(
    x=JP_Sales,
    y=reorder(Name, JP_Sales),
    fill=Platform
  )
) +
  geom_bar(stat="identity") +
  labs(y="Name", x="Japan Sales (in million USD)") +
  ggtitle("Top 11 Games in Japan's Sales")


#EU Sales
EUsales <- vgsales %>%
  arrange(desc(EU_Sales))


ggplot(
  head(EUsales, 11),
  aes(
    x=EU_Sales,
    y=reorder(Name, EU_Sales),
    fill=Platform
  )
) +
  geom_bar(stat="identity") +
  labs(
    y="Name",
    x="EU Sales (in million USD)") +
  ggtitle("Top 11 Games in EU's Sales")


#Other Sales

othersales <- vgsales %>%
  arrange(desc(Other_Sales))

ggplot(
  head(othersales, 11),
  aes(
    x=Other_Sales,
    y=reorder(Name, Other_Sales),
    fill=Platform
  )
) +
  geom_bar(stat="identity") +
  labs(
    y="Name",
    x="Other Sales (in million USD)") +
  ggtitle("Top 11 Games in Other Sales")


#Making a small nintendo only set
smallnin <- nintendo %>%
  select(Global_Sales, Platform, Genre, Name)


#Genre Predictor

model2 <- lm(Global_Sales ~  Genre, data=smallnin)

summary(model2)


#Platform Predictor
model3 <- lm(Global_Sales ~  Platform , data=smallnin)

summary(model3)


#Two predictors
model <- lm(Global_Sales ~  Platform + Genre, data=smallnin)

summary(model)


#Looking at Releases Per yer
releasesperyear <- vgsales %>%
  select(Year, Genre, Name) %>%
  group_by(Year, Genre) %>% 
  summarise(n = n())


releasesperyear

ggplot(data=releasesperyear, aes(x=Year, y=n, fill=Genre)) +
  geom_bar(position='stack', stat="identity", width = 0.8) + 
  theme(axis.text.x = element_text(angle=90, vjust=0.5, hjust=1)) +
  ggtitle("Number of Releases from all Publishers from 1980 to 2016") +
  xlab("Year") + ylab("Number of Releases") 


#looking at Non-Nintendo Data
nonintendo <- vgsales %>%
  filter(Publisher != 'Nintendo') %>%
  arrange(desc(Global_Sales))

nonintendo

ggplot(
  head(nonintendo, 11),
  aes(
    x=Global_Sales,
    y=reorder(Name, Global_Sales),
    fill=Platform
  )
) +
  geom_bar(stat="identity") +
  labs(
    y="Name",
    x="Global Sales (in million USD)") +
  ggtitle("Top 11 Games in Non-Nintendo Global Sales")


#Looking at only 2008 - 2009
twoyears <- vgsales %>%
  filter(Year == "2008" | Year == "2009")

twoyears

ggplot(
  head(twoyears, 10),
  aes(
    x=Global_Sales,
    y=reorder(Name, Global_Sales),
    fill=Platform
  )
) +
  geom_bar(stat="identity") +
  labs(
    y="Name",
    x="Global Sales"
  )


#Genre breakdown

genrecount <- twoyears %>%
  select(Genre, Name, Platform) %>%
  group_by(Genre, Platform) %>% 
  summarise(count = n())


genrecount

ggplot(data=genrecount, aes(x=Genre, y=count, fill = Platform)) +
  geom_bar(position = 'stack', stat="identity", width = 0.8) + 
  theme(axis.text.x = element_text(angle=90, vjust=0.5, hjust=1)) +
  ggtitle("Different Genres Released in 2008 - 2009") +
  xlab("Genre") + ylab("Number of Releases")


#Looking at DS Only sales
ds_sales <- vgsales %>%
  filter(Platform == 'DS') %>%
  group_by(Year) %>%
  summarise(count = n()) %>%
  arrange(Year)

ggplot(data=ds_sales, aes(x=Year, y=count)) +
  geom_bar(stat="identity", width = 0.8) + 
  theme(axis.text.x = element_text(angle=90, vjust=0.5, hjust=1)) +
  ggtitle("Nintendo DS Releases Over Time") +
  xlab("Year") + ylab("Number of Releases")


#sales over time
ggplot(data=ds_sales2, aes(x=Year, y=totalsales)) +
  geom_bar(stat="identity", width = 0.8) + 
  theme(axis.text.x = element_text(angle=90, vjust=0.5, hjust=1)) +
  ggtitle("Nintendo DS Sales Over Time") +
  xlab("Year") + ylab("Total Sales")


#For funsies
filtered <- vgsales %>%
  select(Platform, Year, Genre, Global_Sales) %>%
  filter(Platform == "DS" | Platform == "3DS" | Platform == "GB" | Platform == "GBA" | Platform == "NES" | Platform == "N64" | Platform == "SNES" | 
           Platform == "Wii" | Platform == "WiiU")


ggplot(filtered, aes(x =Year, y =Global_Sales)) + 
  geom_bar(stat = 'identity', fill = "red") + 
  facet_wrap(~ Platform, nrow = 5) +
  theme(axis.text.x = element_text(angle=90, vjust=0.5, hjust=1)) +
  ggtitle("Nintendo Platform Sales Over Time") 