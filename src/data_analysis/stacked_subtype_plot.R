###################################################
library(tidyr)
yaxing <- read.csv("a.csv")
frequency_table <- yaxing %>%
  group_by(year, subtype) %>%
  summarise(count = n(), .groups = 'drop')
wide_format <- frequency_table %>%
  pivot_wider(names_from = subtype, values_from = count, values_fill = list(count = 0))
wide_format <- wide_format %>%
  mutate(Total = rowSums(select(., -year)))
df_long <- pivot_longer(wide_format, cols = starts_with("H7"), names_to = "Subtype", values_to = "Cases")
ggplot(df_long, aes(x = year, y = Cases, fill = Subtype)) +
  geom_area(alpha = 0.5, size = 0.1, colour = "black") +
  scale_fill_manual(
    values = c(
      "H7" = "grey", "H7N1" = "darkgreen", "H7N2" = "blue", "H7N3" = "red",
      "H7N4" = "#9467bd", "H7N5" = "brown", "H7N6" = "yellow", "H7N7" = "pink",
      "H7N8" = "green", "H7N9" = "orange"
    )
  ) +
  labs(
    title = "H7 Subtype Cases Over Time",
    x = "Year",
    y = "Number of sequences",
    fill = "Subtype"
  ) +
  theme_minimal() +
  theme(
    panel.grid = element_blank(),  
    axis.ticks = element_line(color = "black"),  
    axis.line = element_line(color = "black"),  
    axis.text.x = element_text(size = 10, angle = 0, hjust = 1),  
    axis.text.y = element_text(size = 10), 
    plot.title = element_text(size = 14, face = "bold")  
  )
