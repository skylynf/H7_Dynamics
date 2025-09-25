install.packages("devtools"); library(devtools)
install_github("sdellicour/seraphim/unix_OS") # for Unix systems
install_github("sdellicour/seraphim/windows") # for Windows systems

library(seraphim)

install.packages("diagram")
library(diagram)
library(devtools)
library(raster)
library(diagram)
library(rnaturalearth)
library(rnaturalearthdata)
library(seraphim)

#########anser
# 1. Extracting spatio-temporal information embedded in trees

localTreesDirectory = "Extracted_trees"
allTrees = scan(file="H7N7anser.trees", what="", sep="\n", quiet=TRUE)
burnIn = 0
randomSampling = FALSE
nberOfTreesToSample = 100
mostRecentSamplingDatum = 2022.38
coordinateAttributeName = "location"

treeExtractions(localTreesDirectory, allTrees, burnIn, randomSampling, nberOfTreesToSample, mostRecentSamplingDatum, coordinateAttributeName)


# 2. Extracting spatio-temporal information embedded in the MCC tree

source("mccExtractions2.r")
mcc_tre = readAnnotatedNexus("H7N7anserMCC.tree")
mcc_tab = mccExtractions(mcc_tre, mostRecentSamplingDatum)
write.csv(mcc_tab, "YFV_MCC.csv", row.names=F, quote=F)


# 3. Estimating the HPD region for each time slice

nberOfExtractionFiles = nberOfTreesToSample
prob = 0.95; precision = 0.025
startDatum = min(mcc_tab[,"startYear"])

polygons = suppressWarnings(spreadGraphic2(localTreesDirectory, nberOfExtractionFiles, prob, startDatum, precision))


# 4. Defining the different colour scales to use
colour_scale = colorRampPalette(brewer.pal(11,"RdYlGn"))(141)[21:121]
colour_scale = rev(colorRampPalette(brewer.pal(11,"RdYlGn"))(141))[21:121]  # 使用rev()反转颜色顺序

minYear = min(mcc_tab[,"startYear"]); maxYear = max(mcc_tab[,"endYear"])
endYears_indices = (((mcc_tab[,"endYear"]-minYear)/(maxYear-minYear))*100)+1
endYears_colours = colour_scale[endYears_indices]
polygons_colours = rep(NA, length(polygons))
for (i in 1:length(polygons))
{
  date = as.numeric(names(polygons[[i]]))
  polygon_index = round((((date-minYear)/(maxYear-minYear))*100)+1)
  if (!is.na(colour_scale[polygon_index])) {
    polygons_colours[i] = paste0(colour_scale[polygon_index],"00")  #######################################这个地方很重要！！！！
  } else {
    polygons_colours[i] = "gray"  # 当 colour_scale[polygon_index] 为 NA 时，使用灰色作为默认颜色
  }
}


# 5. Co-plotting the HPD regions and MCC tree

template_raster = raster("global_raster.asc")
# 获取全球国家边界数据
world <- ne_countries(scale = "medium", returnclass = "sf")
# 打开绘图设备
dev.new(width=10, height=6.3)
par(mar=c(0,0,0,0), oma=c(1.2,3.5,1,0), mgp=c(0,0.4,0), lwd=0.2, bty="o")
# 绘制模板栅格（如果有的话）
plot(template_raster, col="white", box=F, axes=F, colNA="grey90", legend=F)
# 绘制全球国家边界
plot(world, add = TRUE, col = "white", border = "gray10", lwd = 0.1)

# 加载 geodata 包
library(geodata)
# 设置存储路径（可以更改为你希望的目录）
#path_to_save <- "./gadm_data"  # 你可以设置为其他路径
# 获取巴西一级行政区划数据，并指定存储路径
#borders <- geodata::gadm(country = "BRA", level = 1, path = path_to_save)
#dev.new(width=6, height=6.3)
#par(mar=c(0,0,0,0), oma=c(1.2,3.5,1,0), mgp=c(0,0.4,0), lwd=0.2, bty="o")
#plot(template_raster, col="white", box=F, axes=F, colNA="grey90", legend=F)

# 绘制多边形
for (i in 1:length(polygons))
{
  plot(polygons[[i]], axes=F, col=polygons_colours[i], add=T, border=NA)
}
#plot(borders, add=T, lwd=0.1, border="gray10")
# 绘制传播路径箭头
for (i in 1:dim(mcc_tab)[1])
{
  curvedarrow(cbind(mcc_tab[i,"startLon"],mcc_tab[i,"startLat"]), cbind(mcc_tab[i,"endLon"],mcc_tab[i,"endLat"]), arr.length=0,
              arr.width=0, lwd=0.75, lty=1, lcol="#4169E1", arr.col=NA, arr.pos=FALSE, curve=0.1, dr=NA, endhead=F)
}
# 绘制起始点和结束点
for (i in dim(mcc_tab)[1]:1)
{
  if (i == 1)
  {
    points(mcc_tab[i,"startLon"], mcc_tab[i,"startLat"], pch=16, col=colour_scale[1], cex=0.8)
    points(mcc_tab[i,"startLon"], mcc_tab[i,"startLat"], pch=1, col="gray10", cex=0.8)
  }
  points(mcc_tab[i,"endLon"], mcc_tab[i,"endLat"], pch=16, col=endYears_colours[i], cex=0.8)
  points(mcc_tab[i,"endLon"], mcc_tab[i,"endLat"], pch=1, col="gray10", cex=0.8)
}
# 绘制矩形
rect(xmin(template_raster), ymin(template_raster), xmax(template_raster), ymax(template_raster), xpd=T, lwd=0.2)
# 绘制坐标轴
axis(1, c(ceiling(xmin(template_raster)), floor(xmax(template_raster))), pos=ymin(template_raster), mgp=c(0,0.2,0), cex.axis=0.5, lwd=0, lwd.tick=0.2, padj=-0.8, tck=-0.01, col.axis="gray30")
axis(2, c(ceiling(ymin(template_raster)), floor(ymax(template_raster))), pos=xmin(template_raster), mgp=c(0,0.5,0), cex.axis=0.5, lwd=0, lwd.tick=0.2, padj=1, tck=-0.01, col.axis="gray30")
# 绘制图例
rast = raster(matrix(nrow=1, ncol=2)); rast[1] = min(mcc_tab[,"startYear"]); rast[2] = max(mcc_tab[,"endYear"])

plot(rast, legend.only=T, add=T, col=colour_scale, legend.width=0.5, legend.shrink=0.3, smallplot=c(0.40,0.80,0.14,0.15),
     legend.args=list(text="", cex=0.7, line=0.3, col="gray30"), horizontal=T,
     axis.args=list(cex.axis=0.6, lwd=0, lwd.tick=0.2, tck=-0.5, col.axis="gray30", line=0, mgp=c(0,-0.02,0), at=seq(2000,2024,5)))



#############gall
# 1. Extracting spatio-temporal information embedded in posterior trees

localTreesDirectory = "Tree_extractions"
allTrees = scan(file="H7N7gall.trees", what="", sep="\n", quiet=T)
burnIn = 0
randomSampling = FALSE
nberOfTreesToSample = 100
mostRecentSamplingDatum = 2019.19
coordinateAttributeName = "location"

treeExtractions(localTreesDirectory, allTrees, burnIn, randomSampling, nberOfTreesToSample, mostRecentSamplingDatum, coordinateAttributeName)


# 2. Extracting spatio-temporal information embedded in the MCC tree

source("mccExtractions2.r")
mcc_tre = readAnnotatedNexus("H7N7gallMCC.tree")
mcc_tab = mccExtractions(mcc_tre, mostRecentSamplingDatum)
write.csv(mcc_tab, "YFV_MCC.csv", row.names=F, quote=F)


# 3. Estimating the HPD region for each time slice

nberOfExtractionFiles = nberOfTreesToSample
prob = 0.95; precision = 0.025
startDatum = min(mcc_tab[,"startYear"])

polygons = suppressWarnings(spreadGraphic2(localTreesDirectory, nberOfExtractionFiles, prob, startDatum, precision))


# 4. Defining the different colour scales to use
colour_scale = colorRampPalette(brewer.pal(11,"RdYlGn"))(141)[21:121]
colour_scale = rev(colorRampPalette(brewer.pal(11,"RdYlGn"))(141))[21:121]  # 使用rev()反转颜色顺序

minYear = min(mcc_tab[,"startYear"]); maxYear = max(mcc_tab[,"endYear"])
endYears_indices = (((mcc_tab[,"endYear"]-minYear)/(maxYear-minYear))*100)+1
endYears_colours = colour_scale[endYears_indices]
polygons_colours = rep(NA, length(polygons))
for (i in 1:length(polygons))
{
  date = as.numeric(names(polygons[[i]]))
  polygon_index = round((((date-minYear)/(maxYear-minYear))*100)+1)
  if (!is.na(colour_scale[polygon_index])) {
    polygons_colours[i] = paste0(colour_scale[polygon_index],"00")  #######################################这个地方很重要！！！！
  } else {
    polygons_colours[i] = "gray"  # 当 colour_scale[polygon_index] 为 NA 时，使用灰色作为默认颜色
  }
}


# 5. Co-plotting the HPD regions and MCC tree

template_raster = raster("global_raster.asc")
# 获取全球国家边界数据
world <- ne_countries(scale = "medium", returnclass = "sf")
# 打开绘图设备
dev.new(width=10, height=6.3)
par(mar=c(0,0,0,0), oma=c(1.2,3.5,1,0), mgp=c(0,0.4,0), lwd=0.2, bty="o")
# 绘制模板栅格（如果有的话）
plot(template_raster, col="white", box=F, axes=F, colNA="grey90", legend=F)
# 绘制全球国家边界
plot(world, add = TRUE, col = "white", border = "gray10", lwd = 0.1)

# 加载 geodata 包
library(geodata)
# 设置存储路径（可以更改为你希望的目录）
#path_to_save <- "./gadm_data"  # 你可以设置为其他路径
# 获取巴西一级行政区划数据，并指定存储路径
#borders <- geodata::gadm(country = "BRA", level = 1, path = path_to_save)
#dev.new(width=6, height=6.3)
#par(mar=c(0,0,0,0), oma=c(1.2,3.5,1,0), mgp=c(0,0.4,0), lwd=0.2, bty="o")
#plot(template_raster, col="white", box=F, axes=F, colNA="grey90", legend=F)

# 绘制多边形
for (i in 1:length(polygons))
{
  plot(polygons[[i]], axes=F, col=polygons_colours[i], add=T, border=NA)
}
#plot(borders, add=T, lwd=0.1, border="gray10")
# 绘制传播路径箭头
for (i in 1:dim(mcc_tab)[1])
{
  curvedarrow(cbind(mcc_tab[i,"startLon"],mcc_tab[i,"startLat"]), cbind(mcc_tab[i,"endLon"],mcc_tab[i,"endLat"]), arr.length=0,
              arr.width=0, lwd=0.5, lty=1, lcol="brown", arr.col=NA, arr.pos=FALSE, curve=0.1, dr=NA, endhead=F)
}
# 绘制起始点和结束点
for (i in dim(mcc_tab)[1]:1)
{
  if (i == 1)
  {
    points(mcc_tab[i,"startLon"], mcc_tab[i,"startLat"], pch=16, col=colour_scale[1], cex=0.8)
    points(mcc_tab[i,"startLon"], mcc_tab[i,"startLat"], pch=1, col="gray10", cex=0.8)
  }
  points(mcc_tab[i,"endLon"], mcc_tab[i,"endLat"], pch=16, col=endYears_colours[i], cex=0.8)
  points(mcc_tab[i,"endLon"], mcc_tab[i,"endLat"], pch=1, col="gray10", cex=0.8)
}
# 绘制矩形
rect(xmin(template_raster), ymin(template_raster), xmax(template_raster), ymax(template_raster), xpd=T, lwd=0.2)
# 绘制坐标轴
axis(1, c(ceiling(xmin(template_raster)), floor(xmax(template_raster))), pos=ymin(template_raster), mgp=c(0,0.2,0), cex.axis=0.5, lwd=0, lwd.tick=0.2, padj=-0.8, tck=-0.01, col.axis="gray30")
axis(2, c(ceiling(ymin(template_raster)), floor(ymax(template_raster))), pos=xmin(template_raster), mgp=c(0,0.5,0), cex.axis=0.5, lwd=0, lwd.tick=0.2, padj=1, tck=-0.01, col.axis="gray30")
# 绘制图例
rast = raster(matrix(nrow=1, ncol=2)); rast[1] = min(mcc_tab[,"startYear"]); rast[2] = max(mcc_tab[,"endYear"])

plot(rast, legend.only=T, add=T, col=colour_scale, legend.width=0.5, legend.shrink=0.3, smallplot=c(0.40,0.80,0.14,0.15),
     legend.args=list(text="", cex=0.7, line=0.3, col="gray30"), horizontal=T,
     axis.args=list(cex.axis=0.6, lwd=0, lwd.tick=0.2, tck=-0.5, col.axis="gray30", line=0, mgp=c(0,-0.02,0), at=seq(2000,2024,5)))



##########################wild
# 1. Extracting spatio-temporal information embedded in posterior trees

localTreesDirectory = "Tree_extractions"
allTrees = scan(file="H7N7wild.trees", what="", sep="\n", quiet=T)
burnIn = 0
randomSampling = FALSE
nberOfTreesToSample = 100
mostRecentSamplingDatum = 2022.38
coordinateAttributeName = "location"

treeExtractions(localTreesDirectory, allTrees, burnIn, randomSampling, nberOfTreesToSample, mostRecentSamplingDatum, coordinateAttributeName)


# 2. Extracting spatio-temporal information embedded in the MCC tree

source("mccExtractions2.r")
mcc_tre = readAnnotatedNexus("H7N7wildMCC.tree")
mcc_tab = mccExtractions(mcc_tre, mostRecentSamplingDatum)
write.csv(mcc_tab, "YFV_MCC.csv", row.names=F, quote=F)


# 3. Estimating the HPD region for each time slice

nberOfExtractionFiles = nberOfTreesToSample
prob = 0.95; precision = 0.025
startDatum = min(mcc_tab[,"startYear"])

polygons = suppressWarnings(spreadGraphic2(localTreesDirectory, nberOfExtractionFiles, prob, startDatum, precision))


# 4. Defining the different colour scales to use
colour_scale = colorRampPalette(brewer.pal(11,"RdYlGn"))(141)[21:121]
colour_scale = rev(colorRampPalette(brewer.pal(11,"RdYlGn"))(141))[21:121]  # 使用rev()反转颜色顺序

minYear = min(mcc_tab[,"startYear"]); maxYear = max(mcc_tab[,"endYear"])
endYears_indices = (((mcc_tab[,"endYear"]-minYear)/(maxYear-minYear))*100)+1
endYears_colours = colour_scale[endYears_indices]
polygons_colours = rep(NA, length(polygons))
for (i in 1:length(polygons))
{
  date = as.numeric(names(polygons[[i]]))
  polygon_index = round((((date-minYear)/(maxYear-minYear))*100)+1)
  if (!is.na(colour_scale[polygon_index])) {
    polygons_colours[i] = paste0(colour_scale[polygon_index],"00")  #######################################这个地方很重要！！！！
  } else {
    polygons_colours[i] = "gray"  # 当 colour_scale[polygon_index] 为 NA 时，使用灰色作为默认颜色
  }
}


# 5. Co-plotting the HPD regions and MCC tree

template_raster = raster("global_raster.asc")
# 获取全球国家边界数据
world <- ne_countries(scale = "medium", returnclass = "sf")
# 打开绘图设备
dev.new(width=10, height=6.3)
par(mar=c(0,0,0,0), oma=c(1.2,3.5,1,0), mgp=c(0,0.4,0), lwd=0.2, bty="o")
# 绘制模板栅格（如果有的话）
plot(template_raster, col="white", box=F, axes=F, colNA="grey90", legend=F)
# 绘制全球国家边界
plot(world, add = TRUE, col = "white", border = "gray10", lwd = 0.1)

# 加载 geodata 包
library(geodata)
# 设置存储路径（可以更改为你希望的目录）
#path_to_save <- "./gadm_data"  # 你可以设置为其他路径
# 获取巴西一级行政区划数据，并指定存储路径
#borders <- geodata::gadm(country = "BRA", level = 1, path = path_to_save)
#dev.new(width=6, height=6.3)
#par(mar=c(0,0,0,0), oma=c(1.2,3.5,1,0), mgp=c(0,0.4,0), lwd=0.2, bty="o")
#plot(template_raster, col="white", box=F, axes=F, colNA="grey90", legend=F)

# 绘制多边形
for (i in 1:length(polygons))
{
  plot(polygons[[i]], axes=F, col=polygons_colours[i], add=T, border=NA)
}
#plot(borders, add=T, lwd=0.1, border="gray10")
# 绘制传播路径箭头
for (i in 1:dim(mcc_tab)[1])
{
  curvedarrow(cbind(mcc_tab[i,"startLon"],mcc_tab[i,"startLat"]), cbind(mcc_tab[i,"endLon"],mcc_tab[i,"endLat"]), arr.length=0,
              arr.width=0, lwd=0.75, lty=1, lcol="#4169E1", arr.col=NA, arr.pos=FALSE, curve=0.1, dr=NA, endhead=F)
}
# 绘制起始点和结束点
for (i in dim(mcc_tab)[1]:1)
{
  if (i == 1)
  {
    points(mcc_tab[i,"startLon"], mcc_tab[i,"startLat"], pch=16, col=colour_scale[1], cex=0.8)
    points(mcc_tab[i,"startLon"], mcc_tab[i,"startLat"], pch=1, col="gray10", cex=0.8)
  }
  points(mcc_tab[i,"endLon"], mcc_tab[i,"endLat"], pch=16, col=endYears_colours[i], cex=0.8)
  points(mcc_tab[i,"endLon"], mcc_tab[i,"endLat"], pch=1, col="gray10", cex=0.8)
}
# 绘制矩形
rect(xmin(template_raster), ymin(template_raster), xmax(template_raster), ymax(template_raster), xpd=T, lwd=0.2)
# 绘制坐标轴
axis(1, c(ceiling(xmin(template_raster)), floor(xmax(template_raster))), pos=ymin(template_raster), mgp=c(0,0.2,0), cex.axis=0.5, lwd=0, lwd.tick=0.2, padj=-0.8, tck=-0.01, col.axis="gray30")
axis(2, c(ceiling(ymin(template_raster)), floor(ymax(template_raster))), pos=xmin(template_raster), mgp=c(0,0.5,0), cex.axis=0.5, lwd=0, lwd.tick=0.2, padj=1, tck=-0.01, col.axis="gray30")
# 绘制图例
rast = raster(matrix(nrow=1, ncol=2)); rast[1] = min(mcc_tab[,"startYear"]); rast[2] = max(mcc_tab[,"endYear"])

plot(rast, legend.only=T, add=T, col=colour_scale, legend.width=0.5, legend.shrink=0.3, smallplot=c(0.40,0.80,0.14,0.15),
     legend.args=list(text="", cex=0.7, line=0.3, col="gray30"), horizontal=T,
     axis.args=list(cex.axis=0.6, lwd=0, lwd.tick=0.2, tck=-0.5, col.axis="gray30", line=0, mgp=c(0,-0.02,0), at=seq(2000,2024,5)))





###############################domestic
# 1. Extracting spatio-temporal information embedded in posterior trees

localTreesDirectory = "Tree_extractions"
allTrees = scan(file="H7N7domestic.trees", what="", sep="\n", quiet=T)
burnIn = 0
randomSampling = FALSE
nberOfTreesToSample = 100
mostRecentSamplingDatum = 2021.92
coordinateAttributeName = "location"

treeExtractions(localTreesDirectory, allTrees, burnIn, randomSampling, nberOfTreesToSample, mostRecentSamplingDatum, coordinateAttributeName)


# 2. Extracting spatio-temporal information embedded in the MCC tree

source("mccExtractions2.r")
mcc_tre = readAnnotatedNexus("H7N7domesticMCC.tree")
mcc_tab = mccExtractions(mcc_tre, mostRecentSamplingDatum)
write.csv(mcc_tab, "YFV_MCC.csv", row.names=F, quote=F)


# 3. Estimating the HPD region for each time slice

nberOfExtractionFiles = nberOfTreesToSample
prob = 0.95; precision = 0.025
startDatum = min(mcc_tab[,"startYear"])

polygons = suppressWarnings(spreadGraphic2(localTreesDirectory, nberOfExtractionFiles, prob, startDatum, precision))


# 4. Defining the different colour scales to use
colour_scale = colorRampPalette(brewer.pal(11,"RdYlGn"))(141)[21:121]
colour_scale = rev(colorRampPalette(brewer.pal(11,"RdYlGn"))(141))[21:121]  # 使用rev()反转颜色顺序

minYear = min(mcc_tab[,"startYear"]); maxYear = max(mcc_tab[,"endYear"])
endYears_indices = (((mcc_tab[,"endYear"]-minYear)/(maxYear-minYear))*100)+1
endYears_colours = colour_scale[endYears_indices]
polygons_colours = rep(NA, length(polygons))
for (i in 1:length(polygons))
{
  date = as.numeric(names(polygons[[i]]))
  polygon_index = round((((date-minYear)/(maxYear-minYear))*100)+1)
  if (!is.na(colour_scale[polygon_index])) {
    polygons_colours[i] = paste0(colour_scale[polygon_index],"00")  #######################################这个地方很重要！！！！
  } else {
    polygons_colours[i] = "gray"  # 当 colour_scale[polygon_index] 为 NA 时，使用灰色作为默认颜色
  }
}


# 5. Co-plotting the HPD regions and MCC tree

template_raster = raster("global_raster.asc")
# 获取全球国家边界数据
world <- ne_countries(scale = "medium", returnclass = "sf")
# 打开绘图设备
dev.new(width=10, height=6.3)
par(mar=c(0,0,0,0), oma=c(1.2,3.5,1,0), mgp=c(0,0.4,0), lwd=0.2, bty="o")
# 绘制模板栅格（如果有的话）
plot(template_raster, col="white", box=F, axes=F, colNA="grey90", legend=F)
# 绘制全球国家边界
plot(world, add = TRUE, col = "white", border = "gray10", lwd = 0.1)

# 加载 geodata 包
library(geodata)
# 设置存储路径（可以更改为你希望的目录）
#path_to_save <- "./gadm_data"  # 你可以设置为其他路径
# 获取巴西一级行政区划数据，并指定存储路径
#borders <- geodata::gadm(country = "BRA", level = 1, path = path_to_save)
#dev.new(width=6, height=6.3)
#par(mar=c(0,0,0,0), oma=c(1.2,3.5,1,0), mgp=c(0,0.4,0), lwd=0.2, bty="o")
#plot(template_raster, col="white", box=F, axes=F, colNA="grey90", legend=F)

# 绘制多边形
for (i in 1:length(polygons))
{
  plot(polygons[[i]], axes=F, col=polygons_colours[i], add=T, border=NA)
}
#plot(borders, add=T, lwd=0.1, border="gray10")
# 绘制传播路径箭头
for (i in 1:dim(mcc_tab)[1])
{
  curvedarrow(cbind(mcc_tab[i,"startLon"],mcc_tab[i,"startLat"]), cbind(mcc_tab[i,"endLon"],mcc_tab[i,"endLat"]), arr.length=0,
              arr.width=0, lwd=0.75, lty=1, lcol="brown", arr.col=NA, arr.pos=FALSE, curve=0.1, dr=NA, endhead=F)
}
# 绘制起始点和结束点
for (i in dim(mcc_tab)[1]:1)
{
  if (i == 1)
  {
    points(mcc_tab[i,"startLon"], mcc_tab[i,"startLat"], pch=16, col=colour_scale[1], cex=0.8)
    points(mcc_tab[i,"startLon"], mcc_tab[i,"startLat"], pch=1, col="gray10", cex=0.8)
  }
  points(mcc_tab[i,"endLon"], mcc_tab[i,"endLat"], pch=16, col=endYears_colours[i], cex=0.8)
  points(mcc_tab[i,"endLon"], mcc_tab[i,"endLat"], pch=1, col="gray10", cex=0.8)
}
# 绘制矩形
rect(xmin(template_raster), ymin(template_raster), xmax(template_raster), ymax(template_raster), xpd=T, lwd=0.2)
# 绘制坐标轴
axis(1, c(ceiling(xmin(template_raster)), floor(xmax(template_raster))), pos=ymin(template_raster), mgp=c(0,0.2,0), cex.axis=0.5, lwd=0, lwd.tick=0.2, padj=-0.8, tck=-0.01, col.axis="gray30")
axis(2, c(ceiling(ymin(template_raster)), floor(ymax(template_raster))), pos=xmin(template_raster), mgp=c(0,0.5,0), cex.axis=0.5, lwd=0, lwd.tick=0.2, padj=1, tck=-0.01, col.axis="gray30")
# 绘制图例
rast = raster(matrix(nrow=1, ncol=2)); rast[1] = min(mcc_tab[,"startYear"]); rast[2] = max(mcc_tab[,"endYear"])

plot(rast, legend.only=T, add=T, col=colour_scale, legend.width=0.5, legend.shrink=0.3, smallplot=c(0.40,0.80,0.14,0.15),
     legend.args=list(text="", cex=0.7, line=0.3, col="gray30"), horizontal=T,
     axis.args=list(cex.axis=0.6, lwd=0, lwd.tick=0.2, tck=-0.5, col.axis="gray30", line=0, mgp=c(0,-0.02,0), at=seq(2000,2024,5)))



