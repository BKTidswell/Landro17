
geneGrowthRate <- sample.int(3,1000,replace = TRUE)
geneGrowthDuration <- sample.int(100,1000,replace = TRUE)

gene1Velocity <- sample.int(5,1000,replace = TRUE)
gene2Velocity <- sample.int(5,1000,replace = TRUE)

gene1TravelTime <- sample.int(100,1000,replace = TRUE)
gene2TravelTime <- sample.int(100,1000,replace = TRUE)

size <- geneGrowthRate * geneGrowthDuration
connectionWeight <- (gene1Velocity * gene1TravelTime + gene2Velocity * gene2TravelTime)/2

GDxV <- geneGrowthDuration * gene1Velocity
GRxTT <- geneGrowthRate * gene1TravelTime

plot(GDxV,size)
plot(GDxV, connectionWeight)
plot(GRxTT,size)
plot(GRxTT, connectionWeight)

cor(GDxV,size)
cor(GDxV, connectionWeight)
cor(GRxTT,size)
cor(GRxTT, connectionWeight)

hist(size)
hist(connectionWeight)

startTime <- sample.int(100,1000,replace = TRUE)
plot(startTime,size)
plot(startTime, connectionWeight)
cor(startTime,size)
cor(startTime, connectionWeight)
