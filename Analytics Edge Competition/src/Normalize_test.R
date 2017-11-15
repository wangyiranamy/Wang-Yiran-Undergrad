test <- read.csv("test.csv")
#str(test)
#summary(test)
#summary(unique(test$Case))
test$gend <- as.numeric(test$gender=="Male")
#test$segment[0]
#length(test$segment)
for (i in 1:nrow(test)){
  if (test$segment[i]=="Full-size Pickup") {
    test$car[i]<-1
  } else if ( test$segment[i]=="Midsize Car") {
    test$car[i]<-2
  } else if ( test$segment[i]=="Midsize Luxury Utility segements") {
    test$car[i]<-4
  }else if ( test$segment[i]=="Midsize Utility"){
    test$car[i]<-3
  }else if ( test$segment[i]=="Prestige Luxury Sedan"){
    test$car[i]<-5
  }else {
    test$car[i]<-6
  }}
table(test$segment)
table(test$car)

for (i in 1:nrow(test)){
  if (test$ppark[i]=="Daily") {
    test$newpark[i]<-365
  } else if ( test$ppark[i]=="Monthly") {
    test$newpark[i]<-12
  } else if ( test$ppark[i]=="Never") {
    test$newpark[i]<-0
  }else if ( test$ppark[i]=="Weekly"){
    test$newpark[i]<-52
  }else {
    test$newpark[i]<-1
  }}
# table(test$ppark)
# table(test$newpark)

for (i in 1:nrow(test)){
  if (test$income[i]=="Under $29,999") {
    test$money[i]<-2
  } else if ( test$income[i]=="$30,000 to $39,999") {
    test$money[i]<-3
  } else if ( test$income[i]=="$40,000 to $49,999") {
    test$money[i]<-4
  }else if ( test$income[i]=="$50,000 to $59,999"){
    test$money[i]<-5
  }else if ( test$income[i]=="$60,000 to $69,999"){
    test$money[i]<-6
  }else if ( test$income[i]== "$70,000 to $79,999"){
    test$money[i]<-7
  }else if ( test$income[i]== "$80,000 to $89,999"){
    test$money[i]<-8
  }else if ( test$income[i]== "$90,000 to $99,999"){
    test$money[i]<-9
  }else if ( test$income[i]== "$100,000 to $109,999"){
    test$money[i]<-10
  }else if ( test$income[i]== "$110,000 to $119,999"){
    test$money[i]<-11
  }else if ( test$income[i]== "$120,000 to $129,999"){
    test$money[i]<-12
  }else if ( test$income[i]== "$130,000 to $139,999"){
    test$money[i]<-13
  }else if ( test$income[i]== "$140,000 to $149,999"){
    test$money[i]<-14
  }else if ( test$income[i]== "$150,000 to $159,999"){
    test$money[i]<-15
  }else if ( test$income[i]== "$160,000 to $169,999"){
    test$money[i]<-16
  }else if ( test$income[i]== "$170,000 to $179,999"){
    test$money[i]<-17
  }else if ( test$income[i]== "$180,000 to $189,999"){
    test$money[i]<-18
  }else if ( test$income[i]== "$190,000 to $199,999"){
    test$money[i]<-19
  }else if ( test$income[i]== "$200,000 to $209,999"){
    test$money[i]<-20
  }else if ( test$income[i]== "$220,000 to $219,999"){
    test$money[i]<-21
  }else if ( test$income[i]== "$220,000 to $229,999"){
    test$money[i]<-22
  }else if ( test$income[i]== "$230,000 to $239,999"){
    test$money[i]<-23
  }else if ( test$income[i]== "$240,000 to $249,999"){
    test$money[i]<-24
  }else if ( test$income[i]== "$250,000 to $259,999"){
    test$money[i]<-25
  }else if ( test$income[i]== "$270,000 to $279,999"){
    test$money[i]<-27
  }else if ( test$income[i]== "$280,000 to $289,999"){
    test$money[i]<-28
  }else if ( test$income[i]== "$290,000 to $299,999"){
    test$money[i]<-29
  }else{
    test$money[i]<-30
  }}
# table(test$income)
# table(test$money)

for (i in 1:nrow(test)){
  if (test$educ[i]=="College Graduate (4 Years)") {
    test$educa[i]<-4
  } else if ( test$educ[i]=="Grade School") {
    test$educa[i]<-5
  } else if ( test$educ[i]=="High School") {
    test$educa[i]<-1
  }else if ( test$educ[i]=="Postgraduate College"){
    test$educa[i]<-6
  }else if ( test$educ[i]=="Some College (1-3 Years)"){
    test$educa[i]<-3
  }else{
    test$educa[i]<-2
  }}
# table(test$educ)
# table(test$educa)

for (i in 1:nrow(test)){
  if (test$region[i]=="MW") {
    test$place[i]<-1
  } else if ( test$region[i]=="NE") {
    test$place[i]<-2
  } else if ( test$region[i]=="SE") {
    test$place[i]<-3
  }else if ( test$region[i]=="SW"){
    test$place[i]<-4
  }else{
    test$place[i]<-5
  }}
# table(test$region)
# table(test$place)

for (i in 1:nrow(test)){
  if (test$Urb[i]=="Rural/Country") {
    test$liveplace[i]<-1
  } else if ( test$Urb[i]=="Suburban") {
    test$liveplace[i]<-2
  } else{
    test$liveplace[i]<-3}}
# table(test$Urb)
# table(test$liveplace)

for (i in 1:nrow(test)){
  if (test$miles[i]=="Under 50 Miles") {
    test$distance[i]<-1
  } else if ( test$miles[i]=="51 To 100 Miles") {
    test$distance[i]<-2
  } else if ( test$miles[i]=="101 To 150 Miles") {
    test$distance[i]<-3
  }else if ( test$miles[i]=="151 To 200 Miles"){
    test$distance[i]<-4
  }else if ( test$miles[i]=="201 To 250 Miles"){
    test$distance[i]<-5
  }else if ( test$miles[i]=="251 To 300 Miles"){
    test$distance[i]<-6
  }else if ( test$miles[i]=="301 To 350 Miles "){
    test$distance[i]<-7
  }else if ( test$miles[i]=="351 To 400 Miles"){
    test$distance[i]<-8
  }else{
    test$distance[i]<-9
  }}
# table(test$miles)
# table(test$distance)

for (i in 1:nrow(test)){
  if (test$night[i]=="Under 10%") {
    test$sleep[i]<-1
  } else if ( test$night[i]=="10% To 20%") {
    test$sleep[i]<-2
  } else if ( test$night[i]=="21% To 30%") {
    test$sleep[i]<-3
  }else if ( test$night[i]=="31% To 40%"){
    test$sleep[i]<-4
  }else if ( test$night[i]=="41% To 50%"){
    test$sleep[i]<-5
  }else if ( test$night[i]=="51% To 60%"){
    test$sleep[i]<-6
  }else if ( test$night[i]=="61% To 70%"){
    test$sleep[i]<-7
  }else if ( test$night[i]=="71% To 80%"){
    test$sleep[i]<-8
  }else if ( test$night[i]=="81% To 90%"){
    test$sleep[i]<-9
  }else {
    test$sleep[i]<-10
  }}
# table(test$night)
# table(test$sleep)
for (i in 1:nrow(test)){
  if (test$age[i]=="30 To 39") {
    test$old[i]<-3
  } else if ( test$age[i]=="40 To 49") {
    test$old[i]<-4
  } else if ( test$age[i]=="50 To 59") {
    test$old[i]<-5
  }else if ( test$age[i]=="60 & Over"){
    test$old[i]<-6
  }else{
    test$old[i]<-2
  }}
# table(test$age)
# table(test$old)

#for (i in 1:nrow(test)){
# if (test$Choice[i]=="Ch1") {
#    test$cate[i]<-1
#  } else if ( test$Choice[i]=="Ch2") {
#    test$cate[i]<-2
#  } else if ( test$Choice[i]=="Ch3") {
#    test$cate[i]<-3
#  }else {
##    test$cate[i]<-4
#  }}
#table(test$Choice)
#table(test$cate)

# ncol(test)
# newtest <- test
# #newtest <- test[c(1:63,100:109)]
# summary(newtest)
write.csv(test,"testnormall_2.csv")
# nottoonew <- test[c(1:63,84:94,109)]
# summary(nottoonew)
