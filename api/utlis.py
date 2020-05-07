import json


def load_and_dump_data(data):
    loaded_data = json.dumps(data)
    return json.loads(loaded_data)


def custom_response():
    property_response = {
        "message": "success",
        "data": {
            "items": [
                {
                    "title": "Onyx Hotel",
                    "id": "here:pds:place:840drt3n-c74b2d61e215480bbbbf9ef0cf11387c",
                    "resultType": "place",
                    "address": {
                        "label": "Onyx Hotel, 155 Portland St, Boston, MA 02114-1702, United States",
                        "countryCode": "USA",
                        "countryName": "United States",
                        "state": "Massachusetts",
                        "county": "Suffolk",
                        "city": "Boston",
                        "district": "Downtown Boston",
                        "street": "Portland St",
                        "postalCode": "02114-1702",
                        "houseNumber": "155"
                    },
                    "position": {
                        "lat": 42.36422,
                        "lng": -71.06134
                    },
                    "access": [
                        {
                            "lat": 42.36412,
                            "lng": -71.0615
                        }
                    ],
                    "distance": 527,
                    "categories": [
                        {
                            "id": "100-1000-0000"
                        },
                        {
                            "id": "200-2200-0000"
                        },
                        {
                            "id": "500-5000-0000"
                        },
                        {
                            "id": "500-5000-0053"
                        },
                        {
                            "id": "500-5100-0059"
                        },
                        {
                            "id": "700-7400-0141"
                        },
                        {
                            "id": "700-7400-0284"
                        }
                    ],
                    "contacts": [
                        {
                            "phone": [
                                {
                                    "value": "+16175579955"
                                }
                            ],
                            "tollFree": [
                                {
                                    "value": "+18666606699"
                                }
                            ],
                            "fax": [
                                {
                                    "value": "+16175570005"
                                }
                            ],
                            "www": [
                                {
                                    "value": "http://www.onyxhotel.com"
                                },
                                {
                                    "value": "https://www.ihg.com/kimptonhotels/hotels/us/en/onyx-hotel-boston-ma/bosox/hoteldetail"
                                },
                                {
                                    "value": "https://www.onyxhotel.com/?cm_mmc=YextLocal-_-cp-_-US-_-ONX"
                                }
                            ],
                            "email": [
                                {
                                    "value": "talktous@onyxhotel.com"
                                }
                            ]
                        }
                    ],
                    "openingHours": [
                        {
                            "text": [
                                "Mon-Sun: 00:00 - 24:00"
                            ],
                            "isOpen": True,
                            "structured": [
                                {
                                    "start": "T000000",
                                    "duration": "PT24H00M",
                                    "recurrence": "FREQ:DAILY;BYDAY:MO,TU,WE,TH,FR,SA,SU"
                                }
                            ]
                        }
                    ]
                },

            ]
        }
    }

    return property_response
