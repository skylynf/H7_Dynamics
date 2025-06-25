install.packages("devtools"); library(devtools)
install_github("sdellicour/seraphim/unix_OS") # for Unix systems
install_github("sdellicour/seraphim/windows") # for Windows systems
setwd("E:/qinliugan/H7/H7N9/beast/continuous/constant")
library(seraphim)

install.packages("diagram")
library(diagram)
library(devtools)
library(raster)
library(diagram)
library(rnaturalearth)
library(rnaturalearthdata)


# 1. Extracting spatio-temporal information embedded in posterior trees

localTreesDirectory = "Tree_extractions"
allTrees = scan(file="H7N9_mafft.trees", what="", sep="\n", quiet=T)
burnIn = 0
randomSampling = FALSE
nberOfTreesToSample = 1000
mostRecentSamplingDatum = 2024.39
coordinateAttributeName = "location"

treeExtractions(localTreesDirectory, allTrees, burnIn, randomSampling, nberOfTreesToSample, mostRecentSamplingDatum, coordinateAttributeName)


# 2. Extracting spatio-temporal information embedded in the MCC tree

source("mccExtractions2.r")
mcc_tre = readAnnotatedNexus("H7N9_mcc.tree")
mcc_tab = mccExtractions(mcc_tre, mostRecentSamplingDatum)
write.csv(mcc_tab, "YFV_MCC.csv", row.names=F, quote=F)


# 3. Estimating the HPD region for each time slice

nberOfExtractionFiles = nberOfTreesToSample
prob = 0.95; precision = 0.025
startDatum = min(mcc_tab[,"startYear"])

polygons = suppressWarnings(spreadGraphic2(localTreesDirectory, nberOfExtractionFiles, prob, startDatum, precision))


# 4. Defining the different colour scales to use
colour_scale = colorRampPalette(brewer.pal(11,"RdYlGn"))(141)[21:121]
colour_scale = rev(colorRampPalette(brewer.pal(11,"RdYlGn"))(141))[21:121]

minYear = min(mcc_tab[,"startYear"]); maxYear = max(mcc_tab[,"endYear"])
endYears_indices = (((mcc_tab[,"endYear"]-minYear)/(maxYear-minYear))*100)+1
endYears_colours = colour_scale[endYears_indices]
polygons_colours = rep(NA, length(polygons))
for (i in 1:length(polygons))
{
  date = as.numeric(names(polygons[[i]]))
  polygon_index = round((((date-minYear)/(maxYear-minYear))*100)+1)
  if (!is.na(colour_scale[polygon_index])) {
    polygons_colours[i] = paste0(colour_scale[polygon_index],"00")
  } else {
    polygons_colours[i] = "gray"
  }
}

for (i in 1:length(polygons))
{
  date = as.numeric(names(polygons[[i]]))
  polygon_index = round((((date-minYear)/(maxYear-minYear))*100)+1)
  if (!is.na(colour_scale[polygon_index])) {
    polygons_colours[i] = paste0(colour_scale[polygon_index],"FF")
  } else {
    polygons_colours[i] = "gray"
  }
}


# 5. Co-plotting the HPD regions and MCC tree

template_raster = raster("global_raster.asc")
world <- ne_countries(scale = "medium", returnclass = "sf")
dev.new(width=10, height=6.3)
par(mar=c(0,0,0,0), oma=c(1.2,3.5,1,0), mgp=c(0,0.4,0), lwd=0.2, bty="o")
plot(template_raster, col="white", box=F, axes=F, colNA="grey90", legend=F)
plot(world, add = TRUE, col = "white", border = "gray10", lwd = 0.1)

library(geodata)
#borders <- geodata::gadm(country = "BRA", level = 1, path = path_to_save)
#dev.new(width=6, height=6.3)
#par(mar=c(0,0,0,0), oma=c(1.2,3.5,1,0), mgp=c(0,0.4,0), lwd=0.2, bty="o")
#plot(template_raster, col="white", box=F, axes=F, colNA="grey90", legend=F)

for (i in 1:length(polygons))
{
  plot(polygons[[i]], axes=F, col=polygons_colours[i], add=T, border=NA)
}
#plot(borders, add=T, lwd=0.1, border="gray10")
for (i in 1:dim(mcc_tab)[1])
{
  curvedarrow(cbind(mcc_tab[i,"startLon"],mcc_tab[i,"startLat"]), cbind(mcc_tab[i,"endLon"],mcc_tab[i,"endLat"]), arr.length=0,
              arr.width=0, lwd=2, lty=1, lcol="gray10", arr.col=NA, arr.pos=FALSE, curve=0.1, dr=NA, endhead=F)
}
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
rect(xmin(template_raster), ymin(template_raster), xmax(template_raster), ymax(template_raster), xpd=T, lwd=0.2)
axis(1, c(ceiling(xmin(template_raster)), floor(xmax(template_raster))), pos=ymin(template_raster), mgp=c(0,0.2,0), cex.axis=0.5, lwd=0, lwd.tick=0.2, padj=-0.8, tck=-0.01, col.axis="gray30")
axis(2, c(ceiling(ymin(template_raster)), floor(ymax(template_raster))), pos=xmin(template_raster), mgp=c(0,0.5,0), cex.axis=0.5, lwd=0, lwd.tick=0.2, padj=1, tck=-0.01, col.axis="gray30")
rast = raster(matrix(nrow=1, ncol=2)); rast[1] = min(mcc_tab[,"startYear"]); rast[2] = max(mcc_tab[,"endYear"])

plot(rast, legend.only=T, add=T, col=colour_scale, legend.width=0.5, legend.shrink=0.3, smallplot=c(0.40,0.80,0.14,0.15),
     legend.args=list(text="", cex=0.7, line=0.3, col="gray30"), horizontal=T,
     axis.args=list(cex.axis=0.6, lwd=0, lwd.tick=0.2, tck=-0.5, col.axis="gray30", line=0, mgp=c(0,-0.02,0), at=seq(2000,2024,5)))





years_to_show <- c(2000, 2005, 2010, 2015, 2020, 2024)
year_indices <- sapply(years_to_show, function(year) {
  index <- round(((year - minYear) / (maxYear - minYear)) * 100) + 1
  index <- max(1, min(index, length(colour_scale)))
  index
})
plot(rast, legend.only=T, add=T, col=colour_scale[year_indices], legend.width=0.5, legend.shrink=0.3, smallplot=c(0.40,0.80,0.14,0.15),
     legend.args=list(text="", cex=0.7, line=0.3, col="gray30"), horizontal=T,
     axis.args=list(cex.axis=0.6, lwd=0, lwd.tick=0.2, tck=-0.5, col.axis="gray30", line=0, mgp=c(0,-0.02,0), at=years_to_show))


plot(rast, legend.only=T, add=T, col=colour_scale, legend.width=0.5, legend.shrink=0.3, smallplot=c(0.40,0.80,0.14,0.15),
     legend.args=list(text="", cex=0.7, line=0.3, col="gray30"), horizontal=T,
     axis.args=list(cex.axis=0.6, lwd=0, lwd.tick=0.2, tck=-0.5, col.axis="gray30", line=0, mgp=c(0,-0.02,0), at=seq(2016.4,2017.2,0.2)))










# 5. Co-plotting the HPD regions and MCC tree

template_raster = raster("global_raster.asc")


world <- ne_countries(scale = "medium", returnclass = "sp")

world <- ne_countries(scale = "medium", returnclass = "sf")

dev.new(width=6, height=6.3)
par(mar=c(0,0,0,0), oma=c(1.2,3.5,1,0), mgp=c(0,0.4,0), lwd=0.2, bty="o")


plot(template_raster, col="white", box=F, axes=F, colNA="grey90", legend=F)


plot(world, add = TRUE, col = "gray80", border = "gray10", lwd = 0.1)


for (i in 1:length(polygons))
{
  plot(polygons[[i]], axes=F, col=polygons_colours[i], add=T, border=NA)
}


for (i in 1:dim(mcc_tab)[1])
{
  curvedarrow(cbind(mcc_tab[i,"startLon"],mcc_tab[i,"startLat"]), cbind(mcc_tab[i,"endLon"],mcc_tab[i,"endLat"]), arr.length=0,
              arr.width=0, lwd=0.2, lty=1, lcol="gray10", arr.col=NA, arr.pos=FALSE, curve=0.1, dr=NA, endhead=F)
}


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


rect(xmin(template_raster), ymin(template_raster), xmax(template_raster), ymax(template_raster), xpd=T, lwd=0.2)


axis(1, c(ceiling(xmin(template_raster)), floor(xmax(template_raster)), pos=ymin(template_raster), mgp=c(0,0.2,0), cex.axis=0.5, lwd=0, lwd.tick=0.2, padj=-0.8, tck=-0.01, col.axis="gray30")
     axis(2, c(ceiling(ymin(template_raster)), floor(ymax(template_raster)), pos=xmin(template_raster), mgp=c(0,0.5,0), cex.axis=0.5, lwd=0, lwd.tick=0.2, padj=1, tck=-0.01, col.axis="gray30")
          
          
          rast = raster(matrix(nrow=1, ncol=2))
          rast[1] = min(mcc_tab[,"startYear"]); rast[2] = max(mcc_tab[,"endYear"])
          plot(rast, legend.only=T, add=T, col=colour_scale, legend.width=0.5, legend.shrink=0.3, smallplot=c(0.40,0.80,0.14,0.15),
               legend.args=list(text="", cex=0.7, line=0.3, col="gray30"), horizontal=T,
               axis.args=list(cex.axis=0.6, lwd=0, lwd.tick=0.2, tck=-0.5, col.axis="gray30", line=0, mgp=c(0,-0.02,0), at=seq(2016.4,2017.2,0.2)))