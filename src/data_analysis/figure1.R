H7 <- read.csv("H7FAO.csv")
data_cleaned <- H7 %>%
  filter(!is.na(year) & year != "")
H7_1 <- data_cleaned %>%  
  group_by(Region,year,month) %>% 
  summarise(
    count = n())
H7_2<- subset(H7,H7$Animaltype=='Domestic')
H7_3 <- H7_2 %>%  
  group_by(Region,year,month) %>% 
  summarise(
    count = n())
H7_4 <- H7_3 %>%
  filter(!is.na(year) & year != "")
library(ggplot2)
library(dplyr)

p1 <- ggplot(H7_1, aes(x = factor(year), y = count, fill = Region, group = interaction(year, month))) +
  geom_bar(stat = "identity", position = "dodge") +
  labs(title = "Animal type = all",
       x = "Year",
       y = "Frequency of event",
       fill = "Region") +
  theme_minimal() +
  theme(
    axis.text.x = element_text(angle = 0, hjust = 0.5),
    axis.line = element_line(color = "black"),
    panel.grid.major = element_blank(),
    panel.grid.minor = element_blank(),
    axis.ticks = element_line(color = "black")
  ) +
  scale_fill_manual(values = c("#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "yellow")) +
  scale_x_discrete(breaks = unique(factor(H7_1$year)))

p2 <- ggplot(H7_4, aes(x = factor(year), y = count, fill = Region, group = interaction(year, month))) +
  geom_bar(stat = "identity", position = "dodge") +
  labs(title = "Animal type = Domestic",
       x = "Year",
       y = "Frequency of event",
       fill = "Region") +
  theme_minimal() +
  theme(
    axis.text.x = element_text(angle = 0, hjust = 0.5),
    axis.line = element_line(color = "black"),
    panel.grid.major = element_blank(),
    panel.grid.minor = element_blank(),
    axis.ticks = element_line(color = "black")
  ) +
  scale_fill_manual(values = c("#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "yellow")) +
  scale_x_discrete(breaks = unique(factor(H7_1$year)))
library(gridExtra)
grid.arrange(p1,p2,ncol= 1)



library(dplyr)
data <- read.csv("epanAfricaqinliuganWAHIS.csv")
summary_data <- data %>%
  group_by(Year) %>%
  summarise(
    Total_Cases = sum(Cases, na.rm = TRUE),
    Total_Killed = sum(Killed, na.rm = TRUE),
    Total_Slaughter = sum(Slaughtered, na.rm = TRUE),
    Total_Deaths = sum(Deaths, na.rm = TRUE)
  )
merged_data <- H7_1 %>%
  left_join(summary_data, by = c("year" = "Year"))
library(scales)
line_data <- merged_data %>%
  group_by(year) %>%
  summarise(
    Total_Cases = mean(Total_Cases),
    Total_Slaughter = mean(Total_Slaughter),
    Total_Killed = mean(Total_Killed),
    Total_Deaths = mean(Total_Deaths)
  )
ggplot() +
  geom_bar(data = merged_data, aes(x = factor(year), y = count, fill = Region, group = interaction(year, month)), 
           stat = "identity", position = "dodge", alpha = 0.7) +
  geom_line(data = line_data, aes(x = factor(year), y = Total_Cases / 10000, color = "Total Cases", group = 1), size = 0.5) +
  geom_line(data = line_data, aes(x = factor(year), y = Total_Slaughter / 10000, color = "Total Slaughter", group = 1), size = 0.5) +
  geom_line(data = line_data, aes(x = factor(year), y = Total_Killed / 10000, color = "Total Killed", group = 1), size = 0.5) +
  geom_line(data = line_data, aes(x = factor(year), y = Total_Deaths / 10000, color = "Total Deaths", group = 1), size = 0.5) +
  scale_y_continuous(
    name = "Frequency of event",
    sec.axis = sec_axis(~ . * 10000, name = "Total Values (Yearly)")
  ) +
  scale_x_discrete(name = "Year", breaks = unique(factor(merged_data$year))) +
  labs(title = "Animal type = all",
       x = "Year",
       y = "Frequency of event",
       fill = "Region",
       color = "Total Values") +
  theme_minimal() +
  theme(
    axis.text.x = element_text(angle = 0, hjust = 0.5),
    axis.line = element_line(color = "black"),
    panel.grid.major = element_blank(),
    panel.grid.minor = element_blank(),
    axis.ticks = element_line(color = "black")
  ) +
  scale_fill_manual(values = c("Africa" = "#1f77b4", "Asia" = "#ff7f0e","North America"="#d62728",
                               "Europe"="#2ca02c","Oceania"="#9467bd","South America"="yellow")) +  
  scale_color_manual(values = c("Total Cases" = "darkgreen", "Total Slaughter" = "purple", "Total Killed" = "brown", "Total Deaths" = "pink"))

data <- read_excel("H7N9人感染.xlsx")

frequency_table <- table(data$Year)

frequency_df <- as.data.frame(frequency_table)

library(ggplot2)


ggplot(frequency_df, aes(x = Var1, y = Freq)) +
  geom_bar(stat = "identity", fill = "orange", color = "orange") +
  labs(x = "Year", y = "Case", title = "") +
  theme_minimal() + theme(
    panel.grid = element_blank(),  
    axis.line = element_line(color = "black"), 
    axis.ticks = element_line(color = "black" ))