setwd("E:/qinliugan/H7/H7N3/beast/jump")

# Load required packages
library(ggplot2)
library(dplyr)
library(sf)
library(grid)
library(rnaturalearth)
# Retrieve world map data
world <- ne_countries(scale = "medium", returnclass = "sf")
world <- world[world$admin != "Antarctica", ]

# Define node coordinates (longitude, latitude)
nodes <- data.frame(
  country = c("NorthAmerica", "EU", "SA", "Asia",  "AF","Oceania"),
  long = c(-100, 0,  -60, 90,  30,140 ),
  lat = c(40, 50,  -20, 30,  20,-30)
)

# Read path data, Bayes factors and Markov jumps, then categorise jump counts
path<- read_excel("H7N3_jump_reward_result.xlsx",sheet="Sheet1",col_names = TRUE,na = "NA")


# Group markov_jump into discrete ranges
path <- path %>%
  mutate(
    markov_jump_group = case_when(
      markov_jump <= 1 ~ "0-1",
      markov_jump > 1 & markov_jump <= 5 ~ "1-5",
      markov_jump > 5  ~ ">5"
    )
  )

# Merge node data to fetch coordinates for path start/end points
path <- path %>%
  left_join(nodes, by = c("from" = "country")) %>%
  rename(x0 = long, y0 = lat) %>%
  left_join(nodes, by = c("to" = "country")) %>%
  rename(x1 = long, y1 = lat)

# Define arrow style
arrow_style <- arrow(length = unit(0.2, "cm"), type = "closed")

# Draw map and connections
ggplot() +
  geom_sf(data = world, fill = "lightgray", color = "black") +
  geom_point(data = nodes, aes(x = long, y = lat), size = 5, color = "black") +
  geom_text(data = nodes, aes(x = long, y = lat, label = country), vjust = -1, size = 4) +
  geom_curve(data = path, aes(x = x0, y = y0, xend = x1, yend = y1, color = markov_jump_group, linewidth = markov_jump_group),
             curvature = 0.2, arrow = arrow_style) +
  scale_color_manual(values = c("0-1" = "gray", "1-5" = "orange", ">5" = "red")) +
  scale_linewidth_manual(values = c("0-1" = 0.5, "1-5" = 1, ">5" = 1)) +
  theme_minimal() +
  theme(panel.grid = element_blank()) +
  labs(title = "Connections between Regions with Markov Jump Count",
       x = "Longitude", y = "Latitude") +
  theme(legend.position = "bottom") +
  guides(color = guide_legend(title = "Markov Jump Group"),
         linewidth = guide_legend(title = "Markov Jump Group"))

setwd("E:/qinliugan/H7/H7N3/beast/jump")
########## 3. Bayes factor heatmap
# (Assumes ggplot2 already loaded)
library(ggplot2)
df <- read_excel("H7N3_jump_reward_result.xlsx",sheet="贝叶斯因子",col_names = TRUE,na = "NA")
df$Category <- cut(df$Value,
                   breaks = c(-Inf, 10, 100, Inf),
                   labels = c("<10", "10-100", ">100")
)
df$Category <- cut(df$Value,
                   breaks = c(-Inf, 10, 30,100, Inf),
                   labels = c("<10", "10-30","30-100", ">100")
)
windows()
# windows() may be replaced by X11() on non-Windows systems
p <- ggplot(df, aes(x = TO, y = FROM, fill = Category)) +
  geom_tile(color = "black") +
  scale_fill_manual(values = c("#FFFFCC",  "red")) +
  labs(x = "TO", y = "FROM", fill = "Legend") +
  theme_minimal() +
  theme(
    axis.text.x = element_text(angle = 45, hjust = 1),
    panel.grid.major = element_blank(),
    panel.grid.minor = element_blank()
  )
# Save figure as PDF
ggsave("H7N3_bayes_factor_heatmap.pdf", plot = p,width = 6, height = 5)




library(dplyr)

data <- data.frame(
  Region = c("Africa", "Asia", "Europe", "North America", "Oceania","South America"),
  Value = c(11.95, 280.213, 160.476, 456.726, 12.922,98.636)
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
  scale_fill_manual(values = c("Africa" = "#1f77b4", 
                               "Asia" = "#ff7f0e", 
                               "Europe" = "#2ca02c", 
                               "North America" = "#d62728", 
                               "South America" = "#9467bd",
                               "Oceania"="grey")) +
  labs(title = "Time virus spends in region (%)")


ANSERIFORMES	588.333	57.61 
Environment	2.749	0.27 
GALLIFORMES	371.014	36.33 
other	59.17	5.79 

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
