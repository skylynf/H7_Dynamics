library(ggplot2)
library(dplyr)
data <- data.frame(
  Region = c("ANSERIFORMES", "Environment", "GALLIFORMES", "Other"),
  Value = c(588.333, 2.749, 371.014, 59.17)
)
data <- data %>%
  mutate(Percentage = Value / sum(Value) * 100)
ggplot(data, aes(x = 2, y = Percentage, fill = Region)) +
  geom_bar(stat = "identity", width = 1, color = "black", linewidth = 0.5) +
  coord_polar(theta = "y") +
  xlim(0.5, 2.5) +
  theme_void() +
  theme(
    legend.position = "right",
    legend.title = element_text(size = 12, face = "bold"),
    legend.text = element_text(size = 10),
    plot.title = element_text(size = 16, face = "bold", hjust = 0.5)
  ) +
  geom_text(aes(label = Percentage), 
            position = position_stack(vjust = 0.5), 
            color = "black", size = 4, fontface = "bold") +
  scale_fill_manual(values = c("ANSERIFORMES" = "#1f77b4", 
                               "GALLIFORMES" = "#ff7f0e", 
                               "Environment" = "#2ca02c", 
                                
                               "Other" = "#9467bd"
                               )) +
  labs(title = "Time virus spends in host (%)")
