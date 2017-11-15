library(leaps)
?regsubsets
train <- train[,c(1:83,95:99,110:154)]
which(colnames(train)=="age1")
S <- mlogit.data(train,shape="wide",choice="Choice",sep="",varying=c(4:83,89:132),alt.levels=c("Ch1","Ch2","Ch3","Ch4"),id.var="Case")
S$cate
summary(S)
summary(train)
S$cate <- as.numeric(S$cate==TRUE)
which (colnames(S)=="CC")
which (colnames(S)=="Price")
model1 <- regsubsets(cate~.-Case-No-Task-chid-alt, data=S,nvmax = 30,method = "forward")
model2 <- regsubsets(cate~age+gender+educ+distance+night+region+Urb+ppark+money+year+car,data=train,nvmax = 10,method = "forward")
summary(model1)
which.min((summary(model2))$bic)
which.min((summary(model1))$bic)
coef(model1,25)

library(rpart)
library(rpart.plot)
set.seed(8)
model3 <-rpart(cate~.-Case-No-Task-chid-alt-Ch1-Ch2-Ch3-Ch4-Choice,data=S)
prp(model3)
prp(model3,type=4,extra=2)
predict1 <-predict(model3,newdata = S, type="class")
predict1
table(predict1, S$cate)


###### Random Forest ###########
S$cate
library("randomForest")
set.seed(8)
rf <- randomForest(Choice~CC+GN+NS+BU+FA+LD+BZ+FC+FP+RP+PP+KA+SC+TS+NV+MA+LB+AF+HU+Price+age+gender+educ+distance+night+money+region+Urb+ppark+year+car,data = S, nodesize = 50, ntree = 100)
summary(S)
?randomForest
summary(rf)
?predict
Prediction <- predict(rf, newdata = S)
Prediction
Prediction <-as.double(Prediction)
PredRf <- matrix(Prediction,nrow=4, ncol=14250)
PredRf <-t(PredRf)
colnames(PredRf) <- c("Ch1", "Ch2", "Ch3","Ch4")

###### Cart ########

library(rpart)
library(rpart.plot)
cart1 <- rpart(as.factor(cate)~GN+NS+BU+FA+LD+BZ+FC+FP+RP+PP+KA+SC+TS+NV+MA+LB+AF+HU+Price+age+gender+educ+distance+night+money+region+Urb+ppark,data=S) #fast : X mostly are binary
summary(cart1)
cart1
prp(cart1) #same var occur at may points on the tree
prp(cart1, type = 1) #label all nodes
prp(cart1, type = 4,extra=4) 
predictcart1 <- predict(cart1, newdata=S, type='class')
predictcart1
# testIndexes <- which(folds==3,arr.ind=TRUE)
# testData <- S[testIndexes, ]
# trainData <- S[-testIndexes, ]
# set.seed(8)
# rf <- randomForest(Choice~GN+NS+BU+FA+LD+BZ+FC+FP+RP+PP+KA+SC+TS+NV+MA+LB+AF+HU+Price+age+gender+educ+distance+night+money+region+Urb+ppark,data = trainData, nodesize = 50, ntree = 100)
# summary(rf)
# Prediction <- predict(rf, newdata = testData, type="class")
# Prediction <-as.double(Prediction)
# PredRf <- matrix(Prediction,nrow=4, ncol=nrow(testData)/4)
# PredRf <-t(PredRf)
# colnames(PredRf) <- c("Ch1", "Ch2", "Ch3","Ch4")
# ActualChoice <- subset(testData, testData$Choice==TRUE)[,c("Ch1","Ch2","Ch3","Ch4")]
# ActualChoice <-as.matrix(ActualChoice)
# (-1*mean(log(PredRf[model.matrix(~ ActualChoice + 0) - PredRf > 0])))


folds <- cut(seq(1,nrow(S)),breaks=10,labels=FALSE)
tot <-0
for(k in 1:10){
  #Segement your data by fold using the which() function
  testIndexes <- which(folds==k,arr.ind=TRUE)
  testData <- S[testIndexes, ]
  trainData <- S[-testIndexes, ]
  set.seed(8)
  Mn<- mnlogit(Choice~GN+NS+BU+FA+LD+BZ+FC+FP+RP+PP+KA+SC+TS+NV+MA+LB+AF+HU+Price+age+gender+educ+money+region+Urb+ppark,data=S)
  Prediction <- predict(Mn, newdata = testData)
  # Prediction <-as.double(Prediction)
  # PredRf <- matrix(Prediction,nrow=4, ncol=14250)
  # PredRf <-t(PredRf)
  # colnames(PredRf) <- c("Ch1", "Ch2", "Ch3","Ch4")
  ActualChoice <- subset(testData, testData$Choice==TRUE)[,c("Ch1","Ch2","Ch3","Ch4")]
  ActualChoice <-as.matrix(ActualChoice)
  tot <- tot +(-1*mean(log(PredRf[model.matrix(~ ActualChoice + 0) - PredRf > 0])))
  #Use the test and train data partitions however you desire...
}
tot/10

