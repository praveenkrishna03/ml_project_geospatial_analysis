import joblib
import torch
from transformers import BertTokenizer, BertModel

tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained('bert-base-uncased')

def check_places(sentence, label_dict):
    sentence_lower = sentence.lower()
    for key, word_list in label_dict.items():
        for word in word_list:
            if word.lower() in sentence_lower:
                print(f"Label: {key}, Word: {word}")
                return key

def check_with_model(sentence:str):
    tokens = tokenizer.encode(sentence, add_special_tokens=True)
    tokens_tensor = torch.tensor([tokens])
    model.eval()
    with torch.no_grad():
        outputs = model(tokens_tensor)
    pooled_output = outputs[1]
    pooled_output = pooled_output.numpy()
    print("Pooled output:", pooled_output)
    pooled_output_reshaped = pooled_output.reshape(1, -1)
    model_rf = joblib.load('random_forest_model.joblib')
    output = model_rf.predict(pooled_output_reshaped)
    output = int(output[0])
    return output

def get_label(sentence:str):
    label_dict = {
    0: [
        'Western Ghats', 'Eastern Ghats', 'Vindhya Satpura', 'Aravalli Range',
        'Appalachian Mountains', 'Black Forest', 'Ardennes', 'Cévennes National Park',
        'Jiuzhaigou Valley', 'Beech Forests of Apennines', 'Yakushima Island',
        'Trossachs National Park', 'Carpathian Mountains', 'Great Smoky Mountains',
        'Dandenong Ranges', 'Harz Mountains', 'Eifel National Park', 'Białowieża Forests',
        'Dordogne', 'Harz National Park', 'Peak District', 'Bieszczady Mountains',
        'Tatra Mountains','forest'
    ],
    1: [
        'Sundarbans', 'Vembanad-Kol Wetland', 'Chilika', 'Godavari-Krishna Mangroves',
        'Bhitarkanika Mangroves', 'Pichavaram Mangrove Forest', 'Mangrove Forests of Goa',
        'Kerala Backwaters', 'Bhitar Kanika Mangroves', 'Krishna Wildlife Sanctuary',
        'Coringa Wildlife Sanctuary', 'Netravali Wildlife Sanctuary',
        'Point Calimere Wildlife and Bird Sanctuary', 'Sindhudurg Mangroves', 'Kolleru', 'Digha-Sankarpur Development Authority', 'Cauvery Wildlife Sanctuary',
        'Everglades National Park', 'Okavango Delta', 'Amazon River Basin', 'Danube Delta',
        'Kakadu National Park', 'Sundarbans', 'Florida Everglades', 'Okefenokee Swamp',
        'Pantanal', 'Mekong Delta', 'Tonle Sap', 'Niger Delta', 'Sundarbans',
        'Guiana Shield', 'New Orleans', 'Zambezi Delta', 'Sundarbans',
        'Kinabatangan River', 'Gulf Coast', 'Yellow Sea','swamp'
    ],
    2: [
        'Leh', 'kargil', 'Shimla', 'Manali', 'Kullu', 'Lahaul', 'Spiti', 'Mussoorie',
        'Nainital', 'Auli', 'Badrinath', 'Kedarnath', 'Jammu and Kashmir', 'Srinagar',
        'Gulmarg', 'Pahalgam', 'Sonamarg', 'Tawang', 'Gangtok', 'Nathula Pass', 'Tsomgo',
        'Dhauladhar Range', 'Kashmir Valley', 'Doda District', 'North Sikkim', 'Manali-Leh Highway',
        'Auli', 'Alps', 'Rocky Mountains', 'Himalayas', 'Andes', 'Southern Alps', 'Sierra Nevada',
        'Caucasus Mountains', 'Japanese Alps', 'Tatra Mountains', 'Canadian Rockies', 'Patagonian Andes',
        'Scandinavian Mountains', 'Southern Alps', 'Cascades Range', 'Ural Mountains','snow','glacier'
    ],
    3: [
        'Great Plains of North America', 'Pampas of South America',
        'Sahel region of Africa', 'Loess Plateau of China', '   Ukraine'
    ],
    4: [
        'Ratnagiri and Devgad', 'Darjeeling', 'Coorg', 'Munnar', 'Wayanad', 'Thekkady',
        'Tiruchirappalli and Theni', 'Kollam and Thrissur', 'Napa Valley', 'Provence',
        'Valencia', 'Mendoza', 'Kent', 'Yarra Valley', 'São Paulo', 'Douro Valley',
        'Hawkes Bay', 'Stellenbosch', 'Chiang Mai', 'Alentejo', 'Bordeaux', 'Yunnan Province',
        'Cape Winelands', 'Hawaii', 'Andalusia', 'Central Valley', 'Mekong Delta', 'Columbia Valley',
        'Puglia', 'Marsabit County', 'Canterbury Plains', 'Campania'
    ],
    5: [
        'Ganges', 'Brahmaputra', 'Godavari', 'Yamuna', 'Krishna River', 'Kaveri', 'Chilika',
        'Vembanad', 'Wular', 'Hussain Sagar', 'Dal', 'Loktak', 'Pulicat',
        'Sambhar', 'Hemis', 'Superior', 'Victoria', 'Caspian Sea', 'Huron',
        'Michigan', 'Tanganyika', 'Baikal', 'Great Salt', 'Malawi', 'Titicaca',
        'Erie', 'Ontario', 'Ladoga', 'Onega', 'Winnipeg', 'Maracaibo',
        'Tana', 'Chad', 'Eyre', 'Te Anau','water','river','lake'
    ]
    }

    model_match = {
        0:'Deciduous Woodlands',
        1:'Littoral/Swamp',
        2:'Snowfall/ Glacial Region',
        3:'Current Fallow',
        4:'Plantation/ Orchard',
        5:'Waterbodies-Spread',
    }

    map_match = {
        0 : 'deciduous_woodlands',
        1 : 'littoral_swamp',
        2 : 'snowfall',
        3 : 'current_fallow',
        4 : 'plantation',
        5 : 'waterbodies'
    }

    main_list = []
    diction = {}
    diction['user_query'] = sentence
    output = check_places(sentence,label_dict)
    if output:
        print(model_match[int(output)])
        diction['label'] = model_match[int(output)]
        diction['map_link'] = map_match[int(output)]
        return diction
    output = check_with_model(sentence)
    print(model_match[int(output)])
    diction['label'] = model_match[int(output)]
    diction['map_link'] = map_match[int(output)]

    print(diction)
    return diction

if __name__ == '__main__':
    sentence = 'Show me areas having water in kerala'
    get_label(sentence)