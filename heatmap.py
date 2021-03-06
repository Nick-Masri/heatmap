import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
"""
Heatmap code takes inputs for station data, including longitude, latitude, available parking, idle vehicles, 
arrival demand, and departure demand per station. The program then performs a calculation based on this data to give 
each station a "score", which allows it to be placed and shown on a heatmap with other stations based on the condition
it is in and the need for rebalancing. The more highlighted it is, the worse of a condition it is in. Ideally, all
stations are a flat blue. It then either shows the heatmap file or saves it to a local folder, with the files being .png
and having dimensions of 640 x 480 pixels. 

INPUTS: 
- .csv file containing ordered information for each station, including
      longitude
      latitude
      available parking
      idle vehicles
      expected arrivals
      expected departures
  look at sample data given for structure needed

- time start (integer)

        OR
        
- time start (integer)

- (58,) ordered list of idle_vehicles

- (58,) ordered list of available_parking

All 3 inputs going into heatmap_run(current_time, idle_vehicles, available_parking)

OUTPUTS:
- shown heatmap file

        OR

- saved heatmap file(s)
"""

points = []

class NaiveForecaster:
    def __init__(self, day_forecast_path, timestepsize, horizon, id_to_idx_path):
        forecaster = np.load(day_forecast_path)
        # ugly hack
        shape = forecaster.shape
        hacky_forecaster = np.zeros((shape[0] * 2, shape[1], shape[2]))
        hacky_forecaster[:shape[0], :, :] = forecaster
        hacky_forecaster[shape[0]:, :, :] = forecaster
        self.forecaster = hacky_forecaster
        # end hack
        self.timestepsize = timestepsize
        self.nsteps = (3600 * 24) / (timestepsize * 60)
        self.horizon = horizon
        self.id_to_idx = np.load(id_to_idx_path).item()
        return

    def predict(self, timestamp, station_ids):
        # print(self.id_to_idx.keys())
        # convert timestep into step
        # time_now = timestamp.time()
        # step = time_now.hour * 3600. + time_now.minute * 60. + time_now.second
        # step = int(np.round((step / self.timestepsize * 60)))
        step = timestamp
        # initialize forecast
        forecast = np.zeros((len(station_ids), len(station_ids), self.horizon))
        # find the idx
        f_index = []  # for which stations do we have a forecast
        new_index = []  # what is their equivalent in the estimator
        for i, station_id in enumerate(station_ids):
            if str(station_id) in self.id_to_idx.keys():
                f_index.append(i)
                new_index.append(self.id_to_idx[str(station_id)])
        f_idx = np.ix_(f_index, f_index)
        idx = np.ix_(new_index, new_index)
        # assign the forecast
        # I hope there was a faster way
        # q = self._get_min_q(self.forecaster, step)
        for i in range(self.horizon):
            # forecast[:, :, i][f_idx] = poisson.ppf(q,self.forecaster[step+i, :, :][idx])
            forecast[:, :, i][f_idx] = self.forecaster[step+i, :, :][idx]
        # print('Forecasted demand: {}'.format(forecast.sum()))
        return forecast


def score(eD, iV, eA, aP):

    demandOut = eD - iV
    demandIn = eA - aP

    if demandOut > demandIn:
        evaluation = 2 * demandOut
    else:
        evaluation = 2 * demandIn

    if evaluation >= 10:
        s = 10
    elif evaluation <= 0:
        s = 0
    else:
        s = evaluation

    return s


def degrees_to_pixels(long, lat, max_width, max_height, locations):

    rangelat = np.max(locations[:, 0]) - np.min(locations[:, 0])
    rangelong = np.max(locations[:, 1]) - np.min(locations[:, 1])

    width = max_width / rangelong
    length = max_height / rangelat

    x = width * (long - np.min(locations[:, 1]))
    y = length * (lat - np.min(locations[:, 0]))
    points.append([x, y])
    return np.array([x, y])


def heatmap_run(current_time, idle_vehicles, available_parking):

    # grab station_mapping for forecaster
    id_to_idx_path_map = './data/10_days/station_mapping.npy'
    # get mean demand for forecaster
    forecast_path = './data/mean_demand_weekday_5min.npy'


    # enter timestepsize
    time_step_size = 5
    # time horizon
    time_horizon = 12


    # initializes naive forecaster
    forecaster_obj = NaiveForecaster(forecast_path, time_step_size, time_horizon, id_to_idx_path_map)

    # grab station states for predict method
    stations = pd.read_csv('./data/stations_state_indexed.csv').set_index('station_id')
    station_ids = stations.index.tolist()
    # set time start for predict method

    ############################
    ############################

    start_time = current_time % 288 # TODO: insert current_time in here for time1, value should never be over 288, use this
    # start_time = 0

    ############################
    ############################

    # gets prediction array
    forecast_prediction = forecaster_obj.predict(start_time, station_ids)

    # print(np.shape(forecast_prediction))  # (58, 58, 12)
    # print(forecast_prediction)

    # gets total demand for each station for the next 12 timesteps
    demand_all = np.zeros([58, 58])
    for _ in range(0, 12):
        demand_all = demand_all + np.sum(forecast_prediction, axis=2)
    # print(np.shape(demand_all)) (58, 58)
    # print(demand_all)

    forecast_departures_demand = np.sum(demand_all, axis=1)
    forecast_arrivals_demand = np.sum(demand_all, axis=0)

    # print(np.shape(forecast_departures_demand))  # (58,)
    # print(np.shape(forecast_arrivals_demand))  # (58,)

    # df = pd.DataFrame(demand_all)
    # df.to_csv("hour_demand_forecast.csv")

    # FIXME: Code not implemented with simulator fully yet, figure out how to import specific data from above below

    # image size settings
    imageWidth = 640
    imageHeight = 480

    # reading in data from the static csv sample data
    data = pd.read_csv('./data/stations_state_indexed.csv')
    data["demand"] = forecast_departures_demand  # changes data in the csv to the forecast data
    data["arrivals"] = forecast_arrivals_demand  # changes data in the csv to the forecast data

    if np.shape(available_parking) != (0,):
        data["available_parking"] = available_parking
    if np.shape(idle_vehicles) != (0,):
        data["idle_vehicles"] = idle_vehicles

    # 6 and 7 are lat and long
    # 0, 1, 2, and 4 are all car data
    # 0 = arrivals, 1 = available_parking, 2 = demand, 4 = idle_vehicles
    # 3, although not given, states the station ID numbers
    # For basic data, only 6 and 7 are needed, all other data will be retrieved from simulator.

    I = [0, 1, 2, 4, 6, 7]

    data2 = data.iloc[:, I]
    locations = data2.iloc[:, [4, 5]].values
    # print(locations)
    data3 = data2.values
    env = np.zeros((len(data3), imageWidth, imageHeight))

    points = []

    pix = np.zeros((imageWidth, imageHeight, 2))
    for j in range(imageWidth):
        for k in range(imageHeight):
            pix[j][k][1] = k
            pix[j][k][0] = j


    for i, value in enumerate(data3):
        s = score(value[2], value[3], value[0], value[1])
        coordinates = degrees_to_pixels(value[5], value[4], imageWidth, imageHeight, locations)
        env[i, :, :] = -.005 * ((pix[:, :, 0] - coordinates[0]) ** 2 + (pix[:, :, 1] - coordinates[1]) ** 2)
        env[i, :, :] = s * np.exp(env[i, :, :])


    points = np.array(points)
    # print(points)

    grayscale = np.sum(env, axis=0)

    plt.imshow(grayscale.T, cmap='jet')
    plt.gca().invert_yaxis()
    X = locations[:, 1] - np.min(locations[:, 1])
    X = imageWidth * X/np.max(X)
    Y = locations[:, 0] - np.min(locations[:, 0])
    Y = imageHeight * Y / np.max(Y)

    # fig, ax = plt.subplots()
    # ax.scatter(X, Y, s=8, c='w', marker='.')
    # n = data.iloc[:, 3]
    # for i, txt in enumerate(n):
        # ax.annotate(txt, (X[i], Y[i]))


    plt.scatter(X, Y, s=8, c='w', marker='.')
    plt.show()  # FIXME must be commented out to have the file save correctly


    ############################
    ############################

    # plt.title('Test Controller Time: %d' % current_time)  # adds corresponding titles to the pictures before they save
    # plt.savefig('./saved_pictures/heatmap_test%d.png' % current_time, bbox_inches='tight')  # saves pics with diff file names

    ############################
    ############################


# heatmap_run(0, [], [])  # test function run

# score(eD, iV, eA, aP)
# print(score(5.7, 1, 0.7, 4))
# print(score(0.2, 1, 0, 1))
