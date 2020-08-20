import itertools

aTimeList = [ 0 , 10 ]
theDataList = [ 10, 8, 8, 4, 6, 6, 4, 10 ]  

theNumDataPoint = len( theDataList )
theNumTimePoint = len( aTimeList )
theNumTimeSeries = int( theNumDataPoint / theNumTimePoint )

def intersection( aTimeSeries1 , aTimeSeries2 , aTimeList ):
    t1 = aTimeList[0] 
    t2 = aTimeList[1] 
    a1 = aTimeSeries1[0] 
    a2 = aTimeSeries1[1] 
    b1 = aTimeSeries2[0] 
    b2 = aTimeSeries2[1]

    x = t1 + ( t2 - t1 ) * ( a1 - b1 ) / ( ( b2 - b1 ) - ( a2 - a1) )
    y = a1 + ( a2 - a1 ) * ( a1 - b1 ) / ( ( b2 - b1 ) - ( a2 - a1 ) )

    return ( x , y )


def getY( x , aTimeSeries , aTimeList ) :
    x1 = aTimeList[0]
    x2 = aTimeList[1]
    y1 = aTimeSeries[0]
    y2 = aTimeSeries[1]

    y = ( y2 - y1 ) / ( x2 - x1 ) * ( x - x1 ) + y1

    return( y )


def trapezoid( aLowerList , anUpperList ) :
    aHeight = anUpperList[0] - aLowerList[0]
    anUpper = anUpperList[2] - anUpperList[1]
    aLower = aLowerList[2] - aLowerList[1]

    anArea = ( anUpper + aLower ) * aHeight / 2.0 

    return( anArea )

##
## Main routine
##

aTimeSeriesList = []

for i in range( 0, theNumDataPoint , theNumTimePoint ) :
    aTimeSeriesList.append( theDataList[i:i+theNumTimePoint] ) 

# Calculating intersections of all the combinations of two time courses. 

anXlist = []
for ( aTimeSeries1 , aTimeSeries2 ) in list( itertools.combinations( aTimeSeriesList , 2 ) ) :
    ( x , y ) = intersection( aTimeSeries1 , aTimeSeries2 , aTimeList )

    # Only intersections within the time interval
    if aTimeList[0] <= x and x <= aTimeList[1] :
        anXlist.append( x )
        #print( x , y , aTimeSeries1, aTimeSeries2 )

anUpperLowerLimitList = []
for x in sorted( anXlist ) :
    anIntersectionList = []
    for aTimeSeries in aTimeSeriesList :
        y = getY( x , aTimeSeries , aTimeList )
        anIntersectionList.append( [ x, y ] )

    anIntersectionList.sort(key=lambda x:x[1])
    anUpperLowerLimitList.append( anIntersectionList[0] + [ anIntersectionList[-1][1] ] )

aTimeSeriesList.sort(key=lambda x:x[0])
anUpperLowerLimit = [ aTimeList[0] , aTimeSeriesList[0][0] , aTimeSeriesList[-1][0] ]
anUpperLowerLimitList.insert( 0 , anUpperLowerLimit )

aTimeSeriesList.sort(key=lambda x:x[1])
anUpperLowerLimit = [ aTimeList[1] , aTimeSeriesList[0][1] , aTimeSeriesList[-1][1] ]
anUpperLowerLimitList.append( anUpperLowerLimit )  



aSumArea = 0
for i in range( 0 , len( anUpperLowerLimitList ) - 1 ) :
    aLowerList = anUpperLowerLimitList[ i : i+2 ][0]
    anUpperList = anUpperLowerLimitList[ i : i+2 ][1]

    anArea = trapezoid( aLowerList , anUpperList ) 

    aSumArea += anArea
    

print( aSumArea ) 

