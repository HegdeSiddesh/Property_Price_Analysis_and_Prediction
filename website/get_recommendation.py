import pickle as pkl
import argparse
import numpy as np

def fetchSimilar(apartment_name, criteria, k=5):
    
    with open('/home/siddesh/Desktop/Git_Repositories/Property_Price_Analysis_and_Prediction/model/similarity_'+criteria+'.pkl', 'rb') as file:
        sim_matrix = pkl.load(file)

    with open('/home/siddesh/Desktop/Git_Repositories/Property_Price_Analysis_and_Prediction/model/apartment_names.pkl', 'rb') as file:
        apartment_names = pkl.load(file)

    #print(apartment_names)
    
    index = apartment_names.to_list().index(apartment_name)
    #print(f"Index is {index}")
    #print(apartment_names.to_list())
    sorted_indices = np.argsort(sim_matrix[index,:])
    result = []
    for idx in sorted_indices[0:k]:
        print(apartment_names.to_list()[idx])
        result.append(apartment_names.to_list()[idx])
    return result


if __name__=='__main__':
    parser = argparse.ArgumentParser(description='Provide inputs to get similar apartment names based on criteria')
    parser.add_argument('-apartment', type=str, required=True)
    parser.add_argument('-criteria', type=str, choices = ['facilities', 'price_details', 'location_advantage'], required=True)
    parser.add_argument('-top_k', type=int, default=5)

    args = parser.parse_args()
    fetchSimilar(args.apartment, args.criteria, k=args.top_k)
