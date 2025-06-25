library(ggplot2)
library(readxl)
setwd("E:/qinliugan/H7/beast/continuous/brownian/host")
setwd("E:/qinliugan/H7/H7图片汇总/WavefrontDiffusion修改图")
data<- read_excel("结果汇总.xlsx",sheet="median_wavedistance",col_names = T,na = "NA")
ggplot(data, aes(x = time, y = distance, color = group, group = group)) +
  geom_line(size = 1) +
  geom_ribbon(aes(ymin = low, ymax = high, fill = group), alpha = 0.3, color = NA) +
  labs(
       x = "Time (Year)",
       y = "Wavefront distance (km)",
       color = "Group",
       fill = "Group") +
  theme_minimal() + 
  theme(axis.ticks = element_line(color = "black") ,
        axis.line = element_line(color = "black"))+
  scale_color_manual(values = c("ANSERIFORMES" = "black", "GALLIFORMES" = "red")) +
  scale_fill_manual(values = c("ANSERIFORMES" = "#abddff", "GALLIFORMES" = "pink"))+
  ylim(0, 20000)



data<- read_excel("结果汇总.xlsx",sheet="mean_diffusion_coefficient",col_names = T,na = "NA")
ggplot(data, aes(x = time, y = diffusion_coefficient, color = group, group = group)) +
  geom_line(size = 1) +
  geom_ribbon(aes(ymin = low, ymax = high, fill = group), alpha = 0.3, color = NA) +
  labs(title = "",
       x = "Time (Year)",
       y = "Diffusion coefficient (km2/day)",
       color = "Group",
       fill = "Group") +
  theme_minimal() + 
  theme(axis.ticks = element_line(color = "black") ,
        axis.line = element_line(color = "black"))+
  scale_color_manual(values = c("ANSERIFORMES" = "black", "GALLIFORMES" = "red")) +
  scale_fill_manual(values = c("ANSERIFORMES" = "#abddff", "GALLIFORMES" = "pink"))+ylim(0, 2000000)




data<- read_excel("结果汇总.xlsx",sheet="wild_demostic_wavefront",col_names = T,na = "NA")
ggplot(data, aes(x = time, y = distance, color = group, group = group)) +
  geom_line(size = 1) +
  geom_ribbon(aes(ymin = low, ymax = high, fill = group), alpha = 0.3, color = NA) +
  labs(
       x = "Time (Year)",
       y = "Wavefront distance (km)",
       color = "Group",
       fill = "Group") +
  theme_minimal() + 
  theme(axis.ticks = element_line(color = "black") ,
        axis.line = element_line(color = "black")) +
  scale_color_manual(values = c("wild" = "
  scale_fill_manual(values = c("wild" = "
  ylim(0, 20000)



data<- read_excel("结果汇总.xlsx",sheet="wild_domestic_coefficient",col_names = T,na = "NA")
ggplot(data, aes(x = time, y = diffusion_coefficient, color = group, group = group)) +
  geom_line(size = 1) +
  geom_ribbon(aes(ymin = low, ymax = high, fill = group), alpha = 0.3, color = NA) +
  labs(title = "",
       x = "Time (Year)",
       y = "Diffusion coefficient (km²/day)",
       color = "Group",
       fill = "Group") +
  theme_minimal() + 
  theme(axis.ticks = element_line(color = "black"),
        axis.line = element_line(color = "black")) +
  scale_color_manual(values = c("wild" = "
  scale_fill_manual(values = c("wild" = "




########weighted diffusion

data<- read_excel("结果汇总.xlsx",sheet="diffusion_coefficient_weighted",col_names = T,na = "NA")
ggplot(data, aes(x = time, y = diffusion_coefficient, color = group, group = group)) +
  geom_line(size = 1) +
  geom_ribbon(aes(ymin = low, ymax = high, fill = group), alpha = 0.3, color = NA) +
  labs(title = "",
       x = "Time (Year)",
       y = "Diffusion coefficient (km2/day)",
       color = "Group",
       fill = "Group") +
  theme_minimal() + 
  theme(axis.ticks = element_line(color = "black") ,
        axis.line = element_line(color = "black"))+
  scale_color_manual(values = c("ANSERIFORMES" = "black", "GALLIFORMES" = "red")) +
  scale_fill_manual(values = c("ANSERIFORMES" = "#abddff", "GALLIFORMES" = "pink")) +
  ylim(0, 6000000)
data<- read_excel("结果汇总.xlsx",sheet="wild_domestic_weightcoefficient",col_names = T,na = "NA")
ggplot(data, aes(x = time, y = diffusion_coefficient, color = group, group = group)) +
  geom_line(size = 1) +
  geom_ribbon(aes(ymin = low, ymax = high, fill = group), alpha = 0.3, color = NA) +
  labs(title = "",
       x = "Time (Year)",
       y = "Diffusion coefficient (km²/day)",
       color = "Group",
       fill = "Group") +
  theme_minimal() + 
  theme(axis.ticks = element_line(color = "black"),
        axis.line = element_line(color = "black")) +
  scale_color_manual(values = c("wild" = "
  scale_fill_manual(values = c("wild" = "
  ylim(0, 6000000)

