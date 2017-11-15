#mapData = read.csv("correctData.csv")
mapData = read.csv("July_25_2017XYPHIData.csv")
library(ggplot2)
library(dplyr)

allIRData = data.frame(mapData$IR1,mapData$IR2,mapData$IR3,mapData$IR4,mapData$IR5,mapData$IR6,mapData$IR7,mapData$IR8)
allPhotoData = data.frame(mapData$LDR1,mapData$LDR2,mapData$LDR3,mapData$LDR4,mapData$LDR5,mapData$LDR6,mapData$LDR7,mapData$LDR8)

irData <- rowSums(allIRData)/8
photoData <- rowSums(allPhotoData)/8

irAll <- data_frame(mapData$X,mapData$Y,irData)
names(irAll) <- c("X", "Y","IR")
photoAll <- data_frame(mapData$X,mapData$Y,photoData)
names(photoAll) <- c("X", "Y","Photo")

avgIR <- irAll %>% group_by(X,Y) %>% summarize(avgIR = mean(IR))
avgPhoto <- photoAll %>% group_by(X,Y) %>% summarize(avgPhoto = mean(Photo))

hist(irData)
hist(photoData)

max(allIRData)
max(allPhotoData)

#position 1 (49/126)
(unique(mapData$X)[31] + unique(mapData$X)[32]) /2
(unique(mapData$Y)[5] + unique(mapData$Y)[6])/2

#position 2 (49/126)
(unique(mapData$X)[20] + unique(mapData$X)[21])/2
(unique(mapData$Y)[25] + unique(mapData$Y)[26])/2

irData <- avgIR$avgIR
photoData <- avgPhoto$avgPhoto


#x = 355, y = 210
#x ~ 356.2, y ~ 213.5

#linMap <- function(x, from, to)
#  (x - min(x)) / max(x - min(x)) * (to - from) + from

#irData <- rowSums(allIRData)/8
#photoData <- rowSums(allPhotoData)/8

#irData <- (irData - mean(irData))/sd(irData)
#photoData <- (photoData - mean(photoData))/sd(photoData)

area.fit <- numeric(length = length(irData))
bin.fit <- numeric(length = length(irData))
thresIR <- 49
thresPhoto <- 126

#Best for right area size 97 , 175
#Best for 25/75 split is 130 , 225

for (i in 1:length(irData)) {
  if(irData[i] > thresIR && photoData[i] > thresPhoto){
    area.fit[i] <- 0
    bin.fit[i] <- 0
  }
  else if(irData[i] < thresIR && photoData[i] > thresPhoto){
    area.fit[i] <- 1
    bin.fit[i] <- 1
  }
  else if(irData[i] > thresIR && photoData[i] < thresPhoto){
    area.fit[i] <- 2
    bin.fit[i] <- 1
  }
  else if(irData[i] < thresIR && photoData[i] < thresPhoto){
    area.fit[i] <- 3
    bin.fit[i] <- 0
  }
}

#0 == high high (A)
#1 == high light low ir (B)
#2 == low light high ir (D)
#3 == low low (C)

length(avgIR$X)
length(avgIR$Y)
length(bin.fit)

ggplot(avgIR, aes(x = X, y = Y, colour = bin.fit)) +
  geom_point(size = 3, shape = 15)+
  scale_colour_gradient(low = "#A9A9A9", high = "#800020")

table(bin.fit)/length(bin.fit)
table(area.fit)/length(area.fit)

mapData$Fitness <- abs(photoData-irData)

#+
#  scale_colour_gradient2(low = "#FF0000",mid = "#FFFFFF", high = "#00FF00",
#                        midpoint = 1.5)

mapData$IR1[mapData$X > 356.2 & mapData$Y  > 213.5]

optim.Thresh <- function(IRThresh,PhotoThresh,type){
  
  #print(params)
  
  #IRThresh <- params[1]
  #PhotoThresh <- params[2]
  
  area.fit <- numeric(length = length(irData))
  bin.fit <- numeric(length = length(irData))
  
  for (i in 1:length(irData)) {
    if(irData[i] > IRThresh && photoData[i] > PhotoThresh){
      area.fit[i] <- 0
      bin.fit[i] <- 0
    }
    else if(irData[i] < IRThresh && photoData[i] > PhotoThresh){
      area.fit[i] <- 1
      bin.fit[i] <- 1
    }
    else if(irData[i] > IRThresh && photoData[i] < PhotoThresh){
      area.fit[i] <- 2
      bin.fit[i] <- 1
    }
    else if(irData[i] < IRThresh && photoData[i] < PhotoThresh){
      area.fit[i] <- 3
      bin.fit[i] <- 0
    }
  }
  
  good <- table(bin.fit)[2]/length(bin.fit)
  bad <- table(bin.fit)[1]/length(bin.fit)
  
  desire <- (good - (bad/1.5))^2
  
  area.fit[1] <- 0
  area.fit[2] <- 1
  area.fit[3] <- 2
  area.fit[4] <- 3
  
  A <- table(area.fit)[1]/length(bin.fit)
  B <- table(area.fit)[2]/length(bin.fit)
  C <- table(area.fit)[3]/length(bin.fit)
  D <- table(area.fit)[4]/length(bin.fit)
  
  correctArea <- (A - 0.3)^2 + (B - 0.2)^2 + (C - 0.2)^2 + (D - 0.3)^2
  
  #return(correctArea + desire*2)
  #print(IRThresh)
  #print(PhotoThresh)
 if(type == "a"){
    #print(desire)
    return(desire)
  }
 else if(type == "b"){
    #print(correctArea)
    return(correctArea)
  }
}

array.IRThresh <- seq(from = 0, to = 200, by = 10)
array.PhotoThresh <- seq(from = 0, to = 200, by = 10)

optim.df <- expand.grid(list(IR=array.IRThresh, Photo=array.PhotoThresh)) 

optim.df$bin.rsme <- mapply(optim.Thresh,optim.df$IR,optim.df$Photo,"a")
optim.df$area.rmse <- mapply(optim.Thresh,optim.df$IR,optim.df$Photo,"b")

ggplot(optim.df, aes(x = IR, y = Photo, size = bin.rsme,color = area.rmse))+
  geom_point()+
  scale_colour_gradient(low = "#00FF00", high = "#FFFFFF")

optim.df$IR[which.min(optim.df$bin.rsme)] #130      2nd:160  Comp 50/50: 50
optim.df$Photo[which.min(optim.df$bin.rsme)] #225   2nd:162  Comp 50/50: 136
optim.df$IR[which.min(optim.df$area.rmse)] #120     2nd:110
optim.df$Photo[which.min(optim.df$area.rmse)] #145  2nd:127

library(DEoptim)

optim.result <- DEoptim(optim.Thresh, c(20,20), c(200,200))
#Thse are for even divide of the four areas
# 55/138 for 25/75
# 49.3/130.6 for 60/40
# 49/126 for 50/50

#These are for even divide of good and bad
#  131.3/177.8 for 25/75
#  135/142 for 60/40
#  135.3/128.1 for 50/50

#Both
# 102.3/166   for 25/75
optim.result$optim$bestmem
optim.result$optim$bestval

o.result <- optim(c(50,150), optim.Thresh, method="Nelder-Mead")
o.result$par
o.result$val
