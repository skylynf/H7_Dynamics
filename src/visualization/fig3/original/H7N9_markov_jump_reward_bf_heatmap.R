library(ggplot2)
library(dplyr)
library(sf)
library(grid)
library(rnaturalearth)
library(readxl)

world <- ne_countries(scale = "medium", returnclass = "sf")
world <- world[world$admin != "Antarctica", ]

nodes <- data.frame(
  country = c("NorthAmerica", "EU", "SA", "Asia", "AF", "Oceania"),
  long = c(-100, 0, -60, 90, 30, 140),
  lat = c(40, 50, -20, 30, 20, -30)
)

path <- read_excel("jump和reward结果.xlsx", sheet = "地理跳跃", col_names = TRUE, na = "NA")

path <- path %>%
  mutate(
    markov_jump_group = case_when(
      markov_jump <= 1 ~ "0-1",
      markov_jump > 1 & markov_jump <= 5 ~ "1-5"
    )
  )

path <- path %>%
  left_join(nodes, by = c("from" = "country")) %>%
  rename(x0 = long, y0 = lat) %>%
  left_join(nodes, by = c("to" = "country")) %>%
  rename(x1 = long, y1 = lat)

if (nrow(path) == 0) {
  stop("No valid path data available.")
}

if (any(is.na(path$x0)) | any(is.na(path$y0)) | any(is.na(path$x1)) | any(is.na(path$y1))) {
  stop("NA values found in path data.")
}

arrow_style <- arrow(length = unit(0.2, "cm"), type = "closed")

ggplot() +
  geom_sf(data = world, fill = "lightgray", color = "black") +
  geom_point(data = nodes, aes(x = long, y = lat), size = 5, color = "black") +
  geom_text(data = nodes, aes(x = long, y = lat, label = country), vjust = -1, size = 4) +
  geom_curve(data = path, aes(x = x0, y = y0, xend = x1, yend = y1, color = markov_jump_group, linewidth = markov_jump_group),
             curvature = 0.2, arrow = arrow_style) +
  scale_color_manual(values = c("0-1" = "gray", "1-5" = "orange")) +
  scale_linewidth_manual(values = c("0-1" = 0.5, "1-5" = 1)) +
  theme_minimal() +
  theme(panel.grid = element_blank()) +
  labs(title = "Connections between Regions with Markov Jump Count",
       x = "Longitude", y = "Latitude") +
  theme(legend.position = "bottom") +
  guides(color = guide_legend(title = "Markov Jump Group"),
         linewidth = guide_legend(title = "Markov Jump Group"))

ggsave("H7N9马尔科夫跳跃pdf", width = 10, height = 8)


library(ggplot2)
library(dplyr)
data <- read_excel("jump和reward结果.xlsx", sheet = "地理reward", col_names = TRUE, na = "NA")

data <- data.frame(
  Region = c("Africa", "Asia", "Europe", "North America", "South America","Oceania"),
  Value = c(62.908, 558.194, 349.981, 275.364, 62.908,)
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
ggsave("地理reward.pdf", width = 10, height = 8)




library(ggplot2)
library(dplyr)
data <- read_excel("jump和reward结果.xlsx", sheet = "宿主reward", col_names = TRUE, na = "NA")

data <- data %>%
  mutate(Percentage = Value / sum(Value) * 100)
ggplot(data, aes(x = 2, y = Percentage, fill = Host)) +
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
                               "Human" = "#d62728", 
                               "Other" = "#9467bd"
                               )) +
  labs(title = "Time virus spends in region (%)")
ggsave("宿主reward.pdf", width = 10, height = 8)



if (!requireNamespace("ggplot2", quietly = TRUE)) install.packages("ggplot2")
library(ggplot2)
df <- read_excel("jump和reward结果.xlsx",sheet="贝叶斯因子",col_names = T,na = "NA")
df$Category <- cut(df$Value,
                   breaks = c(-Inf, 10, 100, Inf),
                   labels = c("<10", "10-100", ">100")
)
windows()
library(ggplot2)

p <- ggplot(df, aes(x = TO, y = FROM, fill = Category)) +
  geom_tile(color = "black") +
  scale_fill_manual(values = c("#FFFFCC",  "orange", "red")) +
  labs(x = "TO", y = "FROM", fill = "Legend") +
  theme_minimal() +
  theme(
    axis.text.x = element_text(angle = 45, hjust = 1),
    panel.grid.major = element_blank(),
    panel.grid.minor = element_blank()
  )
ggsave("H7N9贝叶斯因子热图.pdf", plot = p,width = 6, height = 5)
