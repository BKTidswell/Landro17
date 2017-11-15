library(plotly)
library(xml2)
library(dplyr)
library(car)
library(scatterplot3d)

deg2rad = function(deg) {
  return((pi * deg) / 180)
}

rad2deg = function(rad) {
  return((180 * rad) / pi)
}

distance <- function(x,y){
  xLight <- 189.35
  yLight <- 18.5
  dist <- sqrt((xLight - x)^2 + (yLight - y)^2)
  return(dist)
}

slope2Light <- function(x,y){
  xLight <- 189.35
  yLight <- 18.5
  slope <- (x - xLight)/(y - yLight)
  return(slope)
}

Sys.setenv("plotly_username"="Squidswell")
Sys.setenv("plotly_api_key"="OWPSXcktVJ0cS8QOExFC")

# BKTidswell
# pq752taG3n77bGDUMXPC

# Squidswell
# OWPSXcktVJ0cS8QOExFC

mapData = read.csv("correctData.csv")

funcData <- data.frame(mapData$X,mapData$Y,mapData$PHI,mapData$LDR1,mapData$LDR2,mapData$LDR3,
                       mapData$LDR4,mapData$LDR5,mapData$LDR6,mapData$LDR7,mapData$LDR8)

colnames(funcData) <- c("X","Y","PHI","LDR1","LDR2","LDR3","LDR4","LDR5","LDR6","LDR7","LDR8")

funcData$THETA <- round(((rad2deg(atan(slope2Light(funcData$X,funcData$Y)))) + funcData$PHI) %% 360)

funcData$DIST <- distance(funcData$X,funcData$Y)

thetaData <- funcData %>% group_by(THETA) %>% summarize(mean.LDR1 = mean(LDR2))
p <- 360
axc <- cos(2*pi*thetaData$THETA/p)
axs <- sin(2*pi*thetaData$THETA/p)
Tmodel <- lm(mean.LDR1 ~ poly(THETA,2), data = thetaData)
plot(thetaData$THETA, thetaData$mean.LDR1)
lines(thetaData$THETA,predict(Tmodel), col = 'red')



#ggplot(funcData, aes(x = DIST, y = THETA, color = LDR1)) +
#  geom_point(size = 5, shape = 15) +
#  scale_colour_gradient2(low = "#FF0000",mid = "#FFFFFF", high = "#00FF00",
#                         midpoint = 150)

#ggplot(funcData, aes(x = DIST, y = THETA, color = predict(model2))) +
#  geom_point(size = 6, shape = 15) +
#  scale_colour_gradient2(low = "#FF0000",mid = "#FFFFFF", high = "#00FF00",
#                         midpoint = 150)

#Reviews
#Best models: (cost + sint) * poly(X,4) * poly(Y,3) (1)
#             (I(cost + sint) + poly(X,4) + poly(Y,3))^2 (2)
#        Meh: I((cost + sint)/(DIST^-1))
#Didn't Work: (cost + sint) * DIST (3)
#
#Weird reversals
              
funcData$bin <- bin.fit
funcData$area <- area.fit

p <- 360
cost <- cos(2*pi*funcData$THETA/p)
sint <- sin(2*pi*funcData$THETA/p)
model <- lm(LDR1 ~ (cost + sint) * poly(X,4) * poly(Y,3), data = funcData)
model
hist(predict(model))

d <- plot_ly(funcData, x = ~X, y = ~Y, z = ~PHI, color = ~round(area.fit), 
             colors = 'RdYlGn')%>%
  add_markers() %>%
  layout(title = "This is Data",
         scene = list(xaxis = list(title = 'X'),
                      yaxis = list(title = 'Y'),
                      zaxis = list(title = 'PHI')))

m <- plot_ly(funcData, x = ~X, y = ~Y, z = ~PHI, color = ~round(predict(model)), 
             colors = 'RdYlGn') %>%
  add_markers() %>%
  layout(scene = list( xaxis = list(title = 'X'),
                      yaxis = list(title = 'Y'),
                      zaxis = list(title = 'PHI')))

d
m


r <- plot_ly(distGroup, x = ~DIST, y = ~PHI, z = ~mean.LDR1, 
             colors = 'RdYlGn')%>%
  add_markers() %>%
  layout(title = "This is Data",
         scene = list(xaxis = list(title = 'DIST'),
                      yaxis = list(title = 'PHI'),
                      zaxis = list(title = 'LIGHT')))

r

#scatter3d(x = funcData$X, y = funcData$Y, z = funcData$PHI, 
#          groups = funcData$LDR1, surface = FALSE, grid = FALSE)

#scatterplot3d(x = funcData$X, y = funcData$Y, z = funcData$PHI, highlight.3d = TRUE)

# Create a shareable link to your chart

#htmlwidgets::saveWidget(as.widget(d), "graph.html")

#chart_link_d = api_create(d, filename="data")
#chart_link_d

#chart_link_m = api_create(m, filename="mdata")
#chart_link_m

shift <- 22.5 * 1

tphi <- funcData$PHI[round((funcData$PHI + shift) %% 360) == round((rad2deg(atan(slope2Light(funcData$X,funcData$Y)))))]
tdist <- funcData$DIST[round((funcData$PHI + shift) %% 360) == round((rad2deg(atan(slope2Light(funcData$X,funcData$Y)))))]
tlight <- funcData$LDR1[round((funcData$PHI + shift) %% 360) == round((rad2deg(atan(slope2Light(funcData$X,funcData$Y)))))]

someData <- data_frame(tphi,tdist,tlight)
someData <- arrange(someData, tdist)
plot(someData$tdist[someData$tdist > 50], someData$tlight[someData$tdist > 50])
someP <- lm(someData$tlight[someData$tdist > 50] ~ I(someData$tdist[someData$tdist > 50]^-1))
lines(someData$tdist[someData$tdist > 50], predict(someP))

