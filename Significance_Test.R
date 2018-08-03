#v1 v2 v3
prop.test(n = c(28, 24, 22), x = c(15, 18, 17), alternative = 'two.sided')


#v1 v2
prop.test(n = c(28, 24), x = c(15, 18), alternative = 'two.sided')

#v1 v3
prop.test(n = c(28, 22), x = c(15, 17), alternative = 'two.sided')

#v2 v3
prop.test(n = c(24, 22), x = c(18, 17), alternative = 'two.sided')
