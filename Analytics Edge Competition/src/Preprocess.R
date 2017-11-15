### Preprocess the features: convert factor into reasonable numeric features ###
train <- read.csv("train.csv")
str(train)
summary(train)
summary(unique(train$Case))
train$gend <- as.numeric(train$gender=="Male")
train$segment[0]
length(train$segment)
for (i in 1:nrow(train)){
  if (train$segment[i]=="Full-size Pickup") {
    train$car[i]<-1
  } else if ( train$segment[i]=="Midsize Car") {
    train$car[i]<-2
  } else if ( train$segment[i]=="Midsize Luxury Utility segements") {
    train$car[i]<-4
  }else if ( train$segment[i]=="Midsize Utility"){
    train$car[i]<-3
  }else if ( train$segment[i]=="Prestige Luxury Sedan"){
    train$car[i]<-5
  }else {
    train$car[i]<-6
  }}
table(train$segment)
table(train$car)

for (i in 1:nrow(train)){
  if (train$ppark[i]=="Daily") {
    train$newpark[i]<-365
  } else if ( train$ppark[i]=="Monthly") {
    train$newpark[i]<-12
  } else if ( train$ppark[i]=="Never") {
    train$newpark[i]<-0
  }else if ( train$ppark[i]=="Weekly"){
    train$newpark[i]<-52
  }else {
    train$newpark[i]<-1
  }}
table(train$ppark)
table(train$newpark)

for (i in 1:nrow(train)){
  if (train$income[i]=="Under $29,999") {
    train$money[i]<-2
  } else if ( train$income[i]=="$30,000 to $39,999") {
    train$money[i]<-3
  } else if ( train$income[i]=="$40,000 to $49,999") {
    train$money[i]<-4
  }else if ( train$income[i]=="$50,000 to $59,999"){
    train$money[i]<-5
  }else if ( train$income[i]=="$60,000 to $69,999"){
    train$money[i]<-6
  }else if ( train$income[i]== "$70,000 to $79,999"){
    train$money[i]<-7
  }else if ( train$income[i]== "$80,000 to $89,999"){
    train$money[i]<-8
  }else if ( train$income[i]== "$90,000 to $99,999"){
    train$money[i]<-9
  }else if ( train$income[i]== "$100,000 to $109,999"){
    train$money[i]<-10
  }else if ( train$income[i]== "$110,000 to $119,999"){
    train$money[i]<-11
  }else if ( train$income[i]== "$120,000 to $129,999"){
    train$money[i]<-12
  }else if ( train$income[i]== "$130,000 to $139,999"){
    train$money[i]<-13
  }else if ( train$income[i]== "$140,000 to $149,999"){
    train$money[i]<-14
  }else if ( train$income[i]== "$150,000 to $159,999"){
    train$money[i]<-15
  }else if ( train$income[i]== "$160,000 to $169,999"){
    train$money[i]<-16
  }else if ( train$income[i]== "$170,000 to $179,999"){
    train$money[i]<-17
  }else if ( train$income[i]== "$180,000 to $189,999"){
    train$money[i]<-18
  }else if ( train$income[i]== "$190,000 to $199,999"){
    train$money[i]<-19
  }else if ( train$income[i]== "$200,000 to $209,999"){
    train$money[i]<-20
  }else if ( train$income[i]== "$220,000 to $219,999"){
    train$money[i]<-21
  }else if ( train$income[i]== "$220,000 to $229,999"){
    train$money[i]<-22
  }else if ( train$income[i]== "$230,000 to $239,999"){
    train$money[i]<-23
  }else if ( train$income[i]== "$240,000 to $249,999"){
    train$money[i]<-24
  }else if ( train$income[i]== "$250,000 to $259,999"){
    train$money[i]<-25
  }else if ( train$income[i]== "$270,000 to $279,999"){
    train$money[i]<-27
  }else if ( train$income[i]== "$280,000 to $289,999"){
    train$money[i]<-28
  }else if ( train$income[i]== "$290,000 to $299,999"){
    train$money[i]<-29
  }else{
    train$money[i]<-30
  }}
table(train$income)
table(train$money)

for (i in 1:nrow(train)){
  if (train$educ[i]=="College Graduate (4 Years)") {
    train$educa[i]<-4
  } else if ( train$educ[i]=="Grade School") {
    train$educa[i]<-5
  } else if ( train$educ[i]=="High School") {
    train$educa[i]<-1
  }else if ( train$educ[i]=="Postgraduate College"){
    train$educa[i]<-6
  }else if ( train$educ[i]=="Some College (1-3 Years)"){
    train$educa[i]<-3
  }else{
    train$educa[i]<-2
  }}
table(train$educ)
table(train$educa)

for (i in 1:nrow(train)){
  if (train$region[i]=="MW") {
    train$place[i]<-1
  } else if ( train$region[i]=="NE") {
    train$place[i]<-2
  } else if ( train$region[i]=="SE") {
    train$place[i]<-3
  }else if ( train$region[i]=="SW"){
    train$place[i]<-4
  }else{
    train$place[i]<-5
  }}
table(train$region)
table(train$place)

for (i in 1:nrow(train)){
  if (train$Urb[i]=="Rural/Country") {
    train$liveplace[i]<-1
  } else if ( train$Urb[i]=="Suburban") {
    train$liveplace[i]<-2
  } else{
    train$liveplace[i]<-3}}
table(train$Urb)
table(train$liveplace)

for (i in 1:nrow(train)){
  if (train$miles[i]=="Under 50 Miles") {
    train$distance[i]<-1
  } else if ( train$miles[i]=="51 To 100 Miles") {
    train$distance[i]<-2
  } else if ( train$miles[i]=="101 To 150 Miles") {
    train$distance[i]<-3
  }else if ( train$miles[i]=="151 To 200 Miles"){
    train$distance[i]<-4
  }else if ( train$miles[i]=="201 To 250 Miles"){
    train$distance[i]<-5
  }else if ( train$miles[i]=="251 To 300 Miles"){
    train$distance[i]<-6
  }else if ( train$miles[i]=="301 To 350 Miles "){
    train$distance[i]<-7
  }else if ( train$miles[i]=="351 To 400 Miles"){
      train$distance[i]<-8
  }else{
    train$distance[i]<-9
  }}
table(train$miles)
table(train$distance)

for (i in 1:nrow(train)){
  if (train$night[i]=="Under 10%") {
    train$sleep[i]<-1
  } else if ( train$night[i]=="10% To 20%") {
    train$sleep[i]<-2
  } else if ( train$night[i]=="21% To 30%") {
    train$sleep[i]<-3
  }else if ( train$night[i]=="31% To 40%"){
    train$sleep[i]<-4
  }else if ( train$night[i]=="41% To 50%"){
    train$sleep[i]<-5
  }else if ( train$night[i]=="51% To 60%"){
    train$sleep[i]<-6
  }else if ( train$night[i]=="61% To 70%"){
    train$sleep[i]<-7
  }else if ( train$night[i]=="71% To 80%"){
    train$sleep[i]<-8
  }else if ( train$night[i]=="81% To 90%"){
    train$sleep[i]<-9
  }else {
    train$sleep[i]<-10
  }}
table(train$night)
table(train$sleep)
for (i in 1:nrow(train)){
  if (train$age[i]=="30 To 39") {
    train$old[i]<-3
  } else if ( train$age[i]=="40 To 49") {
    train$old[i]<-4
  } else if ( train$age[i]=="50 To 59") {
    train$old[i]<-5
  }else if ( train$age[i]=="60 & Over"){
    train$old[i]<-6
  }else{
    train$old[i]<-2
  }}
table(train$age)
table(train$old)



#### Run the Normalize_test and Normalize_train codes before process the following ####

newtrain <- train
#newtrain <- train[c(1:63,100:109)]
summary(newtrain)
write.csv(newtrain,"newtrainnorm.csv")
#write.csv(newtrain,"newtestnorm.csv")


