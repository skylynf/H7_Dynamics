library(ggplot2)
library(dplyr)
library(sf)
library(grid)

world <- ne_countries(scale = "medium", returnclass = "sf")
world <- world[world$admin != "Antarctica", ]

nodes <- data.frame(
  country = c("NA", "EU", "SA", "Asia",  "AF"),
  long = c(-100, 0,  -60, 90,  30 ),
  lat = c(40, 50,  -20, 30,  20)
)

path <- data.frame(
  from = c("SA", "SA", "NA", "AF", "AF", "SA", "Asia", "EU","EU","NA","NA","NA","SA","Asia","AF","AF","Asia","EU","EU","Asia"),
  to = c("AF", "Asia", "AF", "SA", "NA", "EU", "SA", "NA","NA","EU","Asia","SA","NA","NA","EU","Asia","AF","AF","Asia","EU"),
  markov_jump = c(1.67E-02, 3.29E-02, 4.01E-02, 4.32E-02, 4.61E-02, 6.44E-02,
                  7.84E-02,0.101,0.28,0.297,0.898,1.005,
                  1.199,1.728,2.178,2.395,3.564,4.426,6.908,7.986)
)
write.csv(path,"jump结果.csv")
path <- path %>%
  mutate(
    markov_jump_group = case_when(
      markov_jump <= 1 ~ "0-1",
      markov_jump > 1 & markov_jump <= 5 ~ "1-5",
      markov_jump > 5  ~ ">5"
    )
  )

path <- path %>%
  left_join(nodes, by = c("from" = "country")) %>%
  rename(x0 = long, y0 = lat) %>%
  left_join(nodes, by = c("to" = "country")) %>%
  rename(x1 = long, y1 = lat)

arrow_style <- arrow(length = unit(0.2, "cm"), type = "closed")

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








library(ggplot2)
library(dplyr)

data <- data.frame(
  Region = c("Africa", "Asia", "Europe", "North America", "South America"),
  Value = c(62.908, 558.194, 349.981, 275.364, 62.908)
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
                               "South America" = "
  labs(title = "Time virus spends in region (%)")



setwd("E:/qinliugan/H7/beast/geo/jump")
if (!requireNamespace("ggplot2", quietly = TRUE)) install.packages("ggplot2")
library(ggplot2)
df <- read_excel("H7贝叶斯因子结果.xlsx",sheet="Sheet1",col_names = T,na = "NA")
df$Category <- cut(df$Value,
                   breaks = c(-Inf, 10, 30,100, Inf),
                   labels = c("<10", "10-30","30-100", ">100")
)
windows()

p <- ggplot(df, aes(x = TO, y = FROM, fill = Category)) +
  geom_tile(color = "black") +
  scale_fill_manual(values = c("#FFFFCC",  "orange", "red","#800026")) +
  labs(x = "TO", y = "FROM", fill = "Legend") +
  theme_minimal() +
  theme(
    axis.text.x = element_text(angle = 45, hjust = 1),
    panel.grid.major = element_blank(),
    panel.grid.minor = element_blank()
  )
ggsave("H7贝叶斯因子热图.pdf", plot = p,width = 6, height = 5)

