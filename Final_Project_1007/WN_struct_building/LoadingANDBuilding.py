'''
This module loads in all NYPD collisions data into a City class.
functions:
load_data
  load_intersection
  load_HighTunBri
    FileNameSet
    FILEload
    DescriptionCleaning
    DATAcleaning
    Handling_xa0
    RenameColumn
    ADDprecinctCode
    UPPERCase
class:
  LoadingbyStructure
    building_borough
    building_road
    building_bridge
    building_tunnel
    building_highway
    
Version 1
Copyright:
@ Nan Wu 
@ nw1045@nyu.edu
@ wooginawunan@gmail.com
'''
from WN_struct_building.CityStructure import *
import pandas as pd
import datetime
from datetime import date
def TimeInterval(TimeBegin,TimeEnd):
    '''
    Create a time list from timebegin and timeend
    Args:
      TimeBegin: Loading data from. format:[YYYY,M] example:[2015,1]
      TimeEnd: Loading data end in. format:[YYYY,M] example:[2016,2]
    Return:
      data series from time begin and time end with a 30 day frequency. It should contain all month from start and end.
    Raise:
    
    '''
    start=datetime.date(TimeBegin[0],TimeBegin[1],20)
    end=datetime.date(TimeEnd[0],TimeEnd[1],20)
    return pd.date_range(start,end,freq='30D')
def load_data(path,TimeBegin,TimeEnd):
    '''
    Main function in loading data.
    Args:
      path: data path
      TimeBegin: Loading data from. format:[YYYY,M] example:[2015,1]
      TimeEnd: Loading data end in. format:[YYYY,M] example:[2016,2]
    Return:
      city object. 
    Raise:
      FileNotFoundError
    '''
    print('Building Structures...')
    print('Reading File...')
    print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
    
    ALLDATE=TimeInterval(TimeBegin, TimeEnd)
    area_name=['bk','bx','mn','qn','si']
    Loading=LoadingbyStructure()
    
    for date in ALLDATE:
        for area in area_name:
            print(date.year,date.month,area,'...')
            #raise FileNotFoundError
            print('Loading CSV File about collisions in Intersection...')
            collisions_intersection, factors_intersection = load_intersection(path, str(date.year), str(date.month).zfill(2), area)
            print('Loading CSV File about collisions in HighTunBri...')
            collisions_HighTunBri, factors_HighTunBri = load_HighTunBri(path, str(date.year), str(date.month).zfill(2), area)
            print('Building Borough Information...')
            Loading.building_borough(str(date.year), str(date.month).zfill(2), area, collisions_intersection, factors_intersection,collisions_HighTunBri, factors_HighTunBri )
            print('Building Road Information...')
            Loading.building_road(str(date.year), str(date.month).zfill(2), area,collisions_intersection, factors_intersection,collisions_HighTunBri, factors_HighTunBri)
            print('Building Highway Information...')
            Loading.building_highway(str(date.year), str(date.month).zfill(2), area,collisions_intersection, factors_intersection,collisions_HighTunBri, factors_HighTunBri)
            print('Building Bridge Information...')
            Loading.building_bridge(str(date.year), str(date.month).zfill(2), area,collisions_intersection, factors_intersection,collisions_HighTunBri, factors_HighTunBri)
            print('Building Tunnel Information...')
            Loading.building_tunnel(str(date.year), str(date.month).zfill(2), area,collisions_intersection, factors_intersection,collisions_HighTunBri, factors_HighTunBri)
            print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
    print('Success...')
    
    return Loading.NYC

def load_intersection(path,y,m,area):
    '''
    Intersection related Data Loading
    Args:
       path: data path where the excel documents are stored in.
       y: year string, format 'YYYY'
       m: month string, format 'MM'
       area: area short name in the name of excel documents , available set { 'bk','bx','mn','qn','si' }
    Returns:
       collisions_intersection: data frame  
       factors_intersection: data frame
    Raises: 
       FileNotFoundError
    '''
    #file name set
    file, sheet_n1, sheet_n2 = FileNameSet(y, m, 0)
    #file reading
    collisions_intersection,factors_intersection=FILEload(path,y,m,area,file,sheet_n1,sheet_n2,2,1)
    
    #data cleaning
    collisions_intersection,factors_intersection=DATAcleaning(collisions_intersection,factors_intersection)
    return collisions_intersection,factors_intersection

def load_HighTunBri(path,y,m,area):
    '''
    HiggwayTunnelBridge related Data Loading
    Args:
       path: data path where the excel documents are stored in.
       y: year string, format 'YYYY'
       m: month string, format 'MM'
       area: area short name in the name of excel documents , available set { 'bk','bx','mn','qn','si' }
    Returns:
       collisions_intersection: data frame  
       factors_intersection: data frame
    Raises: 
       FileNotFoundError
    '''
    #file name set
    file, sheet_n1, sheet_n2 = FileNameSet(y, m, 1)

    #file reading
    
    collisions_HighTunBri, factors_HighTunBri= FILEload(path, y, m, area, file, sheet_n1, sheet_n2, 3, 1)
    #data cleaning
    collisions_HighTunBri, factors_HighTunBri =DATAcleaning(collisions_HighTunBri, factors_HighTunBri)
    
    
    return collisions_HighTunBri, factors_HighTunBri

def FILEload(path,y,m,area,file,sheet_n1,sheet_n2,h,s):
    '''
    Loading csv file
    Args:
        path: Data path
        y: year
        m: month
        area: 'bk','bx','mn','qn','si' 
        sheet_n1: sheet name for collisions
        sheet_n2:  sheet name for factors
    Return:
        collisions: dataframe 
        factors: dataframe
    Raise:
        FileNotFoundError
    '''
    collisions = pd.read_excel(''.join([path,y,'_',m,'_col_excel/',area,file]),sheetname=sheet_n1, header=h, skiprows=s)
    factors = pd.read_excel(''.join([path,y,'_',m,'_col_excel/',area,file]),sheetname=sheet_n2, header=h, skiprows=s)
    return collisions,factors

def DATAcleaning(collisions,factors):
    '''
    Cleaning and normalize the data frames
    Args:
        collisions: dataframe 
        factors: dataframe
    Return:
        collisions: dataframe 
        factors: dataframe
        
    '''
    collisions,factors = DescriptionCleaning(collisions,factors)
    factors = RenameColumn(factors)
    factors = ADDprecinctCode(factors,collisions)
    factors = Handling_xa0(factors)
    factors = UPPERCase(factors);
    return collisions,factors

def FileNameSet(y,m,cORf):
    '''
    Set loading file attributes by given year, month and type
    Args:
      y: year
      m: month
      cORf: collisions or factors
    Return:
      filename, sheet name for collisions, sheet name for factors
    Raise:
      ValueError
    '''
    if cORf==1:
        if (y=='2015') & (int(m)<6):   
            return 'hacc.xls','RoadwayCollisions-1','RoadwayVehiclesContrFactors-2'  
        else: 
            return 'hacc-en-us.xlsx' , 'RoadwayCollisions_1', 'RoadwayVehiclesContrFactors_2'
    else:
        if (y=='2015') & (int(m)<6):   
            return 'acc.xls','IntersectCollisions-1','IntersectVehiclesContrFactors-2'
        else: 
            return 'acc-en-us.xlsx' , 'IntersectCollisions_1', 'IntersectVehiclesContrFactors'

def DescriptionCleaning(collisions,factors):
    '''
    Delete all rows without a collisionID or collisionKey.
    In fact, according to our data set, there are some rows of description under the data in the csv file.
    Args:
        collisions: dataframe 
        factors: dataframe
    Return:
        collisions: dataframe 
        factors: dataframe
    '''
    collisions = collisions[collisions.CollisionID.notnull()]
    factors = factors[factors.ColllisionKey.notnull()]
    return collisions,factors



def Handling_xa0(factors):
    '''
    Replace all \xa0 in ContributingFactorDescription
    Args:
        factors: dataframe
    Return:
        factors: dataframe
    '''
    
    factors['ContributingFactorDescription']=factors['ContributingFactorDescription'].fillna('None')
    ContributingFactor=list(factors['ContributingFactorDescription'])
    factors['ContributingFactorDescription']=list(map(lambda i: ContributingFactor[i].replace('\xa0', ''), range(0,len(ContributingFactor))))
    ContributingFactor=list(factors['ContributingFactorDescription'])
    for i in range(0,len(ContributingFactor)):
        if ContributingFactor[i][-1]==' ' :
            ContributingFactor[i]=ContributingFactor[i][:-1] 
    factors['ContributingFactorDescription']=ContributingFactor
    return factors

def RenameColumn(factors):
    '''
    Rename one column
    Args:
        factors: dataframe
    Return:
        factors: dataframe
    '''
    
    return factors.rename(columns={'ColllisionKey':'CollisionKey'})

def ADDprecinctCode(factors,collisions):
    '''
    add OccurrencePrecinctCode to Factor information
    Args:
        factors: dataframe
        collisions: dataframe 
    Return:
        factors: dataframe
        collisions: dataframe 
    
    '''
    return pd.merge(factors,collisions[['OccurrencePrecinctCode','CollisionKey']], how='left', on='CollisionKey')
 
def UPPERCase(factors):
    '''
    Change all letters in string value into Upper case 
    Args:
        factors: dataframe
    Return:
        factors: dataframe
    '''
    factors['VehicleTypeDescription']=factors['VehicleTypeDescription'].fillna('None')
    factors['VehicleTypeDescription']=[z.upper() for z in factors['VehicleTypeDescription']]
    factors['ContributingFactorDescription']=[z.upper() for z in factors['ContributingFactorDescription']]
    return factors

class LoadingbyStructure():
    def __init__(self):
        self.NYC=city()
        self.NYC.init_borough()
    
    def building_borough(self,y,m,area,collisions_intersection, factors_intersection,collisions_HighTunBri, factors_HighTunBri):     
        '''
        Separate the collisions and factors by borough and precinct, store the data in NYC
        All changes will be stored in the global variables 
        Args: NONE
        Returns: NONE
        Raises:  NONE
        '''
        for precinctID in collisions_intersection['OccurrencePrecinctCode'].unique():
            if precinctID not in self.NYC.Borough_Dict[area].precinctList:
                precinct_new=precinct(precinctID)
            else:
                precinct_new=self.NYC.Borough_Dict[area].precinctList[precinctID]
            
            precinct_new.addFactors_Intersection(y, m, factors_intersection.ix[factors_intersection['OccurrencePrecinctCode']==precinctID])
            precinct_new.addCollisions_Intersection(y, m, collisions_intersection.ix[collisions_intersection['OccurrencePrecinctCode']==precinctID])
            self.NYC.Borough_Dict[area].precinctList[precinctID]=precinct_new
        
        for precinctID in collisions_HighTunBri['OccurrencePrecinctCode'].unique():
            if precinctID not in self.NYC.Borough_Dict[area].precinctList:
                precinct_new=precinct(precinctID)
            else:
                precinct_new=self.NYC.Borough_Dict[area].precinctList[precinctID]
            precinct_new.addCollisions_HighTunBri(y, m, 
                                       collisions_HighTunBri.ix[collisions_HighTunBri['OccurrencePrecinctCode']==precinctID],
                                       factors_HighTunBri.ix[factors_HighTunBri['OccurrencePrecinctCode']==precinctID])
            
            
            self.NYC.Borough_Dict[area].addprecinct(precinct_new)
                
    def building_road(self,y,m,area,collisions_intersection, factors_intersection,collisions_HighTunBri, factors_HighTunBri):
        '''
        Separate the collisions and factors by borough and precinct, store the data in NYC
        All changes will be stored in the global variables 
        Args: NONE
        Returns: NONE
        Raises:  NONE
        '''
        all_street=set(collisions_intersection['IntersectingStreet'].unique())|set(collisions_intersection['CrossStreet'].unique())
        for Road in all_street:
            if Road not in self.NYC.Road_Dict:
                Road_new=road(Road)
            else:
                Road_new=self.NYC.Road_Dict[Road]
            
            Marker=list(collisions_intersection.ix[list(collisions_intersection['IntersectingStreet']==Road) or list(collisions_intersection['CrossStreet']==Road)]['CollisionKey'])
            Road_new.addCollisions(y, m, collisions_intersection.ix[list(collisions_intersection['IntersectingStreet']==Road) or list(collisions_intersection['CrossStreet']==Road)],
                                       factors_intersection.ix[list(map(lambda x: x in Marker,factors_intersection['CollisionKey']))])
            self.NYC.add_road(Road_new)
#         
               
        
    def building_highway(self,y,m,area,collisions_intersection, factors_intersection,collisions_HighTunBri, factors_HighTunBri):
        '''
        Separate the collisions and factors by borough and precinct, store the data in NYC
        All changes will be stored in the global variables 
        Args: NONE
        Returns: NONE
        Raises:  NONE
        '''
        for Highway in collisions_HighTunBri.ix[collisions_HighTunBri['RoadwayTypeCode']=='H']['RoadwayName'].unique():
            if Highway not in self.NYC.Highway_Dict:
                Highway_new=highway(Highway)
            else:
                Highway_new=self.NYC.Highway_Dict[Highway]
            
            Marker=list(collisions_HighTunBri.ix[collisions_HighTunBri['RoadwayName']==Highway]['RoadwayReferenceMarker'])
            Highway_new.addCollisions(y, m, collisions_HighTunBri.ix[collisions_HighTunBri['RoadwayName']==Highway], 
                                     factors_HighTunBri.ix[list(map(lambda x: x in Marker,factors_HighTunBri['RoadwayReferenceMarker']))])
            self.NYC.add_highway(Highway_new)
    def building_tunnel(self,y,m,area,collisions_intersection, factors_intersection,collisions_HighTunBri, factors_HighTunBri):
        '''
        Separate the collisions and factors by borough and precinct, store the data in NYC
        All changes will be stored in the global variables 
        Args: NONE
        Returns: NONE
        Raises:  NONE
        '''
        for Tunnel in collisions_HighTunBri.ix[collisions_HighTunBri['RoadwayTypeCode']=='T']['RoadwayName'].unique():
            if Tunnel not in self.NYC.Tunnel_Dict:
                Tunnel_new=tunnel(Tunnel)
            else:
                Tunnel_new=self.NYC.Tunnel_Dict[Tunnel]
            
            Marker=list(collisions_HighTunBri.ix[collisions_HighTunBri['RoadwayName']==Tunnel]['RoadwayReferenceMarker'])
            Tunnel_new.addCollisions(y, m, collisions_HighTunBri.ix[collisions_HighTunBri['RoadwayName']==Tunnel], 
                                     factors_HighTunBri.ix[list(map(lambda x: x in Marker,factors_HighTunBri['RoadwayReferenceMarker']))])
            self.NYC.add_tunnel(Tunnel_new)
    def building_bridge(self,y,m,area,collisions_intersection, factors_intersection,collisions_HighTunBri, factors_HighTunBri):
        '''
        Separate the collisions and factors by borough and precinct, store the data in NYC
        All changes will be stored in the global variables 
        Args: NONE
        Returns: NONE
        Raises:  NONE
        '''
        for Bridge in collisions_HighTunBri.ix[collisions_HighTunBri['RoadwayTypeCode']=='B']['RoadwayName'].unique():
            if Bridge not in self.NYC.Bridge_Dict:
                Bridge_new=bridge(Bridge)
            else:
                Bridge_new=self.NYC.Bridge_Dict[Bridge]
            
            Marker=list(collisions_HighTunBri.ix[collisions_HighTunBri['RoadwayName']==Bridge]['RoadwayReferenceMarker'])
            Bridge_new.addCollisions(y, m, collisions_HighTunBri.ix[collisions_HighTunBri['RoadwayName']==Bridge], 
                                     factors_HighTunBri.ix[list(map(lambda x: x in Marker,factors_HighTunBri['RoadwayReferenceMarker']))]) 
            self.NYC.add_bridge(Bridge_new)


