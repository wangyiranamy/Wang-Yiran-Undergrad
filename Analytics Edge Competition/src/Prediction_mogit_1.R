#### multi-logit regression model ####
train1 <- read.csv("train.csv")
table(train$Choice)
test <- read.csv("test.csv")
#submit <- read.csv("samplesubmission.csv")
newtrain2 <- read.csv("train.csv")
summary(train)
library("mlogit")
S <- mlogit.data(train1,shape="wide",choice="Choice",sep="",varying=c(4:83),alt.levels=c("Ch1","Ch2","Ch3","Ch4"),id.var="Case")
M <- mlogit(Choice~CC+GN+NS+BU+FA+LD+BZ+FC+FP+RP+PP+KA+SC+TS+NV+MA+LB+AF+HU+Price-1,data=S)
summary(M)
summary(S)
ActualChoice <- train[,"Choice"]
P <- predict(M, newdata = S)
P
PredictedChoice <- apply(P, 1, which.max)
PredictedChoice
table(PredictedChoice, ActualChoice)
for (i in 1:nrow(test)){
  test$Ch1 <-0
  test$Ch2 <-1
  test$Ch3 <-0
  test$Ch4 <-0
  test$Choice <- "Ch2"}
T <- mlogit.data(test,shape="wide",choice="Choice",sep="",varying=c(4:83),alt.levels=c("Ch1","Ch2","Ch3","Ch4"),id.var="Case")
P2 <- predict(M, newdata = T)
P2
nrow(P2)
nrow(test)
submit$Ch1 <- P2[,1]
submit$Ch2 <- P2[,2]
submit$Ch3 <- P2[,3]
submit$Ch4 <- P2[,4]
write.csv(submit, "samplesubmission2.csv")
S2 <- mlogit.data(newtrain2,shape="wide",choice="Choice",sep="",varying=c(4:123),alt.levels=c("Ch1","Ch2","Ch3","Ch4"),id.var="Case")
M2 <- mlogit(Choice~CC+GN+NS+BU+FA+LD+BZ+FC+FP+RP+PP+KA+SC+TS+NV+MA+LB+AF+HU+Price+gend-1,data=S2)
summary(M2)


PredictedChoice <- apply(P2, 1, which.max)
M <- mlogit(Choice~CC+GN+NS+BU+FA+LD+BZ+FC+FP+RP+PP+KA+SC+TS+NV+MA+LB+AF+HU+Price-1,rpar=c(CC='n',GN='n',NS='n',BU='n',FA='n',LD='n',BZ='n',FC='n',FP='n',RP='n',PP='n',KA='n',SC='n',TS='n',NV='n',MA='n',LB='n',AF='n',HU='n',Price='n'),panel=TRUE,data=S)
summary(M)
ActualChoice <- subset(train, Task <= 12)[,"Choice"]
P <- predict(M, newdata = S)
PredictedChoice <- apply(P, 1, which.max)
table(PredictedChoice, ActualChoice)

model1 <- glm(Ch1~segment+year+miles+night+gender+age+educ+region+Urb, data = train, family = binomial)
pred1 <- predict(model1, newdata = train, type = "response")
model2 <- glm(Ch2~segment+year+miles+night+gender+age+educ+region+Urb, data = train, family = binomial)
pred2<- predict(model2, newdata = train, type = "response")
model3 <- glm(Ch3~segment+year+miles+night+gender+age+educ+region+Urb, data = train, family = binomial)
pred3<- predict(model3, newdata = train, type = "response")
model4 <- glm(Ch4~segment+year+miles+night+gender+age+educ+region+Urb, data = train, family = binomial)
pred4<- predict(model4, newdata = train, type = "response")
pred1 <- as.matrix(pred1)
pred2 <- as.matrix(pred2)
pred3 <- as.matrix(pred3)
pred4 <- as.matrix(pred4)
pred <- cbind(pred1, pred2)
pred <- cbind(pred, pred3)
pred <- cbind(pred, pred4)
colnames(pred) <- c("pred1","pred2","pred3","pred4")
pred <- matrix(nrow = nrow(train),ncol = 4,colnames <- c("Ch1","Ch2","Ch3","Ch4"))
pred[,1]<-pred1
pred[,2]<-pred2
pred[,3]<-pred3
pred[,4]<-pred4
pred <- as.numeric(pred)
pred
pred <-as.matrix(pred)
PredictedChoice <- apply(pred, 1, which.max)
PredictedChoice
ActualChoice
table(PredictedChoice, ActualChoice)
