#### Multi-logit Regression Model with new features and normalized data #####
submit <- read.csv("samplesubmission.csv")
train <- read.csv("trainnormall_2.csv")
test <- read.csv("testnormall_2.csv")

train <- train[,c(1:83,95:99,110:153)]
test <- test[,c(1:83,95:99,110:153)]
set.seed(8)
train<-train[sample(nrow(train)),]
library("mlogit")
#### Add new Variable to Train
train$age1 <- as.numeric(train$Price1)*train$old
train$age2 <- as.numeric(train$Price2)*train$old
train$age3 <- as.numeric(train$Price3)*train$old
train$age4 <- as.numeric(train$Price4)*train$old
train$gender1 <- as.numeric(train$Price1)*train$gend
train$gender2 <- as.numeric(train$Price2)*train$gend
train$gender3 <- as.numeric(train$Price3)*train$gend
train$gender4 <- as.numeric(train$Price4)*train$gend
train$educ1 <- as.numeric(train$Price1)*train$educa
train$educ2 <- as.numeric(train$Price2)*train$educa
train$educ3 <- as.numeric(train$Price3)*train$educa
train$educ4 <- as.numeric(train$Price4)*train$educa
train$distance1 <- as.numeric(train$Price1)*train$distance
train$distance2 <- as.numeric(train$Price2)*train$distance
train$distance3 <- as.numeric(train$Price3)*train$distance
train$distance4 <- as.numeric(train$Price4)*train$distance
train$night1 <- as.numeric(train$NV1)*train$sleep
train$night2 <- as.numeric(train$NV2)*train$sleep
train$night3 <- as.numeric(train$NV3)*train$sleep
train$night4 <- as.numeric(train$NV4)*train$sleep
train$region1 <- as.numeric(train$Price1)*train$place
train$region2 <- as.numeric(train$Price2)*train$place
train$region3 <- as.numeric(train$Price3)*train$place
train$region4 <- as.numeric(train$Price4)*train$place
train$Urb1 <- as.numeric(train$Price1)*train$liveplace
train$Urb2 <- as.numeric(train$Price2)*train$liveplace
train$Urb3 <- as.numeric(train$Price3)*train$liveplace
train$Urb4 <- as.numeric(train$Price4)*train$liveplace
train$ppark1 <- as.numeric(train$Price1)*train$newpark
train$ppark2 <- as.numeric(train$Price2)*train$newpark
train$ppark3 <- as.numeric(train$Price3)*train$newpark
train$ppark4 <- as.numeric(train$Price4)*train$newpark
train$car1 <- as.numeric(train$Price1)*train$car
train$car2<- as.numeric(train$Price2)*train$car
train$car3 <- as.numeric(train$Price3)*train$car
train$car4 <- as.numeric(train$Price4)*train$car
train$money1 <- train$money/as.numeric(train$Price1)
train$money2<- train$money/as.numeric(train$Price2)
train$money3 <- train$money/as.numeric(train$Price3)
train$money4 <- as.numeric(train$Price4)
train$year1 <- as.numeric(train$Price1)*train$year
train$year2<- as.numeric(train$Price2)*train$year
train$year3 <- as.numeric(train$Price3)*train$year
train$year4 <- as.numeric(train$Price4)*train$year
#### normalize new variables in train

for (j in 110:153){
  for (i in 1:nrow(train)){
    train[i,j] <- ((train[i,j]-min(train[,j]))/(max(train[,j])-min(train[,j])))
  }}
for (j in 4:63){
  for (i in 1:nrow(train)){
    train[i,j] <- ((train[i,j]-min(train[,j]))/(max(train[,j])-min(train[,j])))
  }}


# which(colnames(train)=="age1")
# which(colnames(train)=="year4")
#### create trainset with glm predicted probability
trainglm<-cbind(train,pred)
#### create mlogit train data
S <- mlogit.data(trainglm,shape="wide",choice="Choice",sep="",varying=c(4:83,110:153),alt.levels=c("Ch1","Ch2","Ch3","Ch4"),id.var="Case")
#S <-S[,2:52]
#S <- mlogit.data(train,shape="wide",choice="Choice",sep="",varying=c(4:83,89:132),alt.levels=c("Ch1","Ch2","Ch3","Ch4"),id.var="Case")
S <- mlogit.data(train,shape="wide",choice="Choice",sep="",varying=c(4:83,110:153),alt.levels=c("Ch1","Ch2","Ch3","Ch4"),id.var="Case")
#Randomly shuffle the train data
#library(caTools)
# set.seed(8)
# spl <-sample.split(twittersparse$Neg,SplitRatio = 0.7)
# train <-subset(twittersparse,spl==TRUE)
# test <- subset(twittersparse,spl==FALSE)
# set.seed(8)
# S<-S[sample(nrow(S)),]
which(is.na(S))
folds <- cut(seq(1,nrow(S)),breaks=10,labels=FALSE) #Create 10 equally size folds
#?cut
# Feature Set
#FeatureSet <- c("CC","GN","NS","BU","FA","LD","BZ","FC","FP","RP","PP","KA","SC","TS","NV","MA","LB","AF","HU","Price","age","gender","educ","distance","night","region","Urb","ppark","money","year","car")
#length(FeatureSet)

### Cross Validation
tot <-0
for(k in 1:10){
  #Segement your data by fold using the which() function
  testIndexes <- which(folds==k,arr.ind=TRUE)
  testData <- S[testIndexes, ]
  trainData <- S[-testIndexes, ]
  Mcv <- mlogit(Choice~GN+NS+BU+FA+LD+BZ+FC+FP+RP+PP+KA+SC+TS+NV+MA+LB+AF+HU+Price+age+gender+educ+money+region+Urb+ppark+night,data=trainData)
  Pcv <- as.matrix(predict(Mcv, newdata = testData))
  predglm <-subset(testData, testData$Choice==TRUE)[,c("pred1","pred2","pred3","pred4")]
  Pmix <- Pcv
  Pmix <- 0.95*Pcv +0.05*predglm
  ActualChoice <- subset(testData, testData$Choice==TRUE)[,c("Ch1","Ch2","Ch3","Ch4")]
  ActualChoice <-as.matrix(ActualChoice)
  tot <- tot +(-1*mean(log(Pmix[model.matrix(~ ActualChoice + 0) - Pmix > 0])))
  #Use the test and train data partitions however you desire...
}
tot/10

#1.19179 pred+ original (0.9)
#1.197947 original only
#1.190847 age+gender+educ 
#1.185584 age+gender+educ & pred (0.9) 
#1.186941 age+gender+educ & pred (0.8)
#1.189926 age+gender+educ+money
#1.184549 age+gender+educ+money & pred(0.9)
#1.183094 all-CC-car-night normalized segment+miles+night+educ+region+Urb 0.8
#1.180877 all-CC-car-night normalized segment+miles+night+educ+region+Urb 0.9
#1.180043 all-CC-car-night normalized partially segment+money+year+miles+night+gender+age+educ+region+Urb+ppark 0.9
#1.181346 ‘’‘’ 0.8
#1.187488 ‘’‘’ 0.7
#1.181731 ‘’‘’‘ 0.95
#1.181487 fs 0.9
#1.181147 fs-CC-car 0.9
# 1.181147 normalized all allglm -CC-car
#*******************
#1.180108 changed var 0.9
#1.181659  normalized 0.9
#1.181578 +night norm 0.9
#1.181241 below 0.9
#1.180232 below (new features)
#1.179854 GN+NS+BU+FA+LD+BZ+FC+FP+RP+PP+KA+SC+TS+NV+MA+LB+AF+HU+Price+age+gender+educ+money+region+Urb+ppark
#1.179972 all 31 features 
#1.179972 all 31 features-car-year
#1.179936 all 31 features-car-year-CC GN+NS+BU+FA+LD+BZ+FC+FP+RP+PP+KA+SC+TS+NV+MA+LB+AF+HU+Price+age+gender+educ+money+region+Urb+ppark+night+distance
#1.180053 all 31 features-car-year-night
#1.180161 all 31 features-car-year-distance
#1.180838 all 31 features 0.9
#1.180893 all 31 features-car-year 0.9
#1.180959 all 31 features-car-year-night 0.9
#1.181172 all 31 features-car-year-distance 0.9
#1.18087  all 31 features-car-year-CC 0.9


#s<-cbind(train,pred)
#S <- mlogit.data(s,shape="wide",choice="Choice",sep="",varying=c(4:83,110:153),alt.levels=c("Ch1","Ch2","Ch3","Ch4"),id.var="Case")
#S<-S[,c(1:8,13:45)]
#M_tot <- mlogit(Choice~CC+GN+NS+BU+FA+LD+BZ+FC+FP+RP+PP+KA+SC+TS+NV+MA+LB+AF+HU+Price+age+gender+educ+money+region+Urb+ppark+distance+night+year+car,data=trainData)
M_tot <- mlogit(Choice~GN+NS+BU+FA+LD+BZ+FC+FP+RP+PP+KA+SC+TS+NV+MA+LB+AF+HU+Price+age+gender+educ+money+region+Urb+ppark+night,data=S)
#M_tot <- mlogit(Choice~CC+GN+NS+BU+FA+LD+BZ+FC+FP+RP+PP+KA+SC+TS+NV+MA+LB+AF+HU+Price+age+gender+money,data=S)
M_fs <- mlogit(Choice~GN+NS+BU+FA+LD+BZ+FC+FP+RP+PP+KA+SC+TS+NV+MA+LB+AF+HU+Price+age+gender+ppark+Urb,data=S)
M_mix <-mlogit(Choice~CC+GN+NS+BU+FA+LD+BZ+FC+FP+RP+PP+KA+SC+TS+NV+MA+LB+AF+HU+Price+age+gender+educ,rpar=c(CC='n',GN='n',NS='n',BU='n',FA='n',LD='n',BZ='n',FC='n',FP='n',RP='n',PP='n',KA='n',SC='n',TS='n',NV='n',MA='n',LB='n',AF='n',HU='n',Price='n',age='n',gender='n',educ='n'),panel=TRUE,data=S)
M_mix_1 <-mlogit(Choice~CC+GN+NS+BU+FA+LD+BZ+FC+FP+RP+PP+KA+SC+TS+NV+MA+LB+AF+HU+Price+age+gender+educ,rpar=c(age='n',gender='n',educ='n'),panel=TRUE,data=S)
#M <- mlogit(Choice~"CC+GN",data=S)
summary(M_tot)
summary(M_fs)
summary(M_mix)
summary(M_mix_1)
ActualChoice <- train[,"Choice"]
P <- predict(M_tot, newdata = S)
#Prf <- read.csv("rf_predict_train_50.csv")
PredMix <- 0.9*P+0.1*pred
#PredMix <- 0.9*P+0.1*pred
(-1*mean(log(PredMix[model.matrix(~ ActualChoice + 0) - PredMix > 0])))
(-1*mean(log(Prf[model.matrix(~ ActualChoice + 0) - Prf > 0])))
# nrow(P)
# length(PredictedChoice)
PredictedChoice <- apply(PredMix, 1, which.max)
table(PredictedChoice, ActualChoice)
#table(PredictedChoice)
#?mlogit

#### Add new variables to test
test$age1 <- as.numeric(test$Price1)*test$old
test$age2 <- as.numeric(test$Price2)*test$old
test$age3 <- as.numeric(test$Price3)*test$old
test$age4 <- as.numeric(test$Price4)*test$old
test$gender1 <- as.numeric(test$Price1)*test$gend
test$gender2 <- as.numeric(test$Price2)*test$gend
test$gender3 <- as.numeric(test$Price3)*test$gend
test$gender4 <- as.numeric(test$Price4)*test$gend
test$educ1 <- as.numeric(test$Price1)*test$educa
test$educ2 <- as.numeric(test$Price2)*test$educa
test$educ3 <- as.numeric(test$Price3)*test$educa
test$educ4 <- as.numeric(test$Price4)*test$educa
test$distance1 <- as.numeric(test$Price1)*test$distance
test$distance2 <- as.numeric(test$Price2)*test$distance
test$distance3 <- as.numeric(test$Price3)*test$distance
test$distance4 <- as.numeric(test$Price4)*test$distance
test$night1 <- as.numeric(test$NV1)*test$sleep
test$night2 <- as.numeric(test$NV2)*test$sleep
test$night3 <- as.numeric(test$NV3)*test$sleep
test$night4 <- as.numeric(test$NV4)*test$sleep
test$region1 <- as.numeric(test$Price1)*test$place
test$region2 <- as.numeric(test$Price2)*test$place
test$region3 <- as.numeric(test$Price3)*test$place
test$region4 <- as.numeric(test$Price4)*test$place
test$Urb1 <- as.numeric(test$Price1)*test$liveplace
test$Urb2 <- as.numeric(test$Price2)*test$liveplace
test$Urb3 <- as.numeric(test$Price3)*test$liveplace
test$Urb4 <- as.numeric(test$Price4)*test$liveplace
test$ppark1 <- as.numeric(test$Price1)*test$newpark
test$ppark2 <- as.numeric(test$Price2)*test$newpark
test$ppark3 <- as.numeric(test$Price3)*test$newpark
test$ppark4 <- as.numeric(test$Price4)*test$newpark
test$car1 <- as.numeric(test$Price1)*test$car
test$car2<- as.numeric(test$Price2)*test$car
test$car3 <- as.numeric(test$Price3)*test$car
test$car4 <- as.numeric(test$Price4)*test$car
test$money1 <- test$money/as.numeric(test$Price1)
test$money2<- test$money/as.numeric(test$Price2)
test$money3 <- test$money/as.numeric(test$Price3)
test$money4 <- as.numeric(test$Price4)
test$year1 <- as.numeric(test$Price1)*test$year
test$year2<- as.numeric(test$Price2)*test$year
test$year3 <- as.numeric(test$Price3)*test$year
test$year4 <- as.numeric(test$Price4)*test$year
###normalize test
which(colnames(test)=="age1")
for (j in 110:153){
  for (i in 1:nrow(test)){
    test[i,j] <- ((test[i,j]-min(test[,j]))/(max(test[,j])-min(test[,j])))
  }}
for (j in 4:63){
  for (i in 1:nrow(test)){
    test[i,j] <- ((test[i,j]-min(test[,j]))/(max(test[,j])-min(test[,j])))
  }}
###
for (i in 1:nrow(test)){
  test$Ch1 <-0
  test$Ch2 <-1
  test$Ch3 <-0
  test$Ch4 <-0
  test$Choice <- "Ch2"}
#which(colnames(test)=="age1")
## create the mlogit test data
T <- mlogit.data(test,shape="wide",choice="Choice",sep="",varying=c(4:83,110:153),alt.levels=c("Ch1","Ch2","Ch3","Ch4"),id.var="Case")
P2 <- predict(M_tot, newdata = T)
P2
#P2rf <- read.csv("rf_predict_test_50.csv")
P7 <- read.csv("samplesubmission7.csv")
P7<-P7[,c(2:5)]
P2Mix <- 0.95*P2+0.05*predtest
P2Mix <- 0.1*predtest+0.9*P2
P2Mix
PredictedChoiceTest <- apply(P2, 1, which.max)
PredictedChoiceTest7 <- apply(P7, 1, which.max)
table(PredictedChoiceTest,PredictedChoiceTest7)
table(PredictedChoiceTest)
table(ActualChoice)

nrow(P2)
nrow(test)
submit$Ch1 <- P2Mix[,1]
submit$Ch2 <- P2Mix[,2]
submit$Ch3 <- P2Mix[,3]
submit$Ch4 <- P2Mix[,4]
write.csv(submit, "samplesubmission16.csv")


S_output <- subset(S, S$Choice=="TRUE")
write.csv(S_output, "S_ouput.csv")
