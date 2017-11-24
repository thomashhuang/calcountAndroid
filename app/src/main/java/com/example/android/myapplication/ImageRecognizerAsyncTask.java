package com.example.android.myapplication;

import android.os.AsyncTask;

import java.util.ArrayList;
import java.util.List;

import clarifai2.api.ClarifaiBuilder;
import clarifai2.api.ClarifaiClient;
import clarifai2.dto.input.ClarifaiImage;
import clarifai2.dto.input.ClarifaiInput;
import clarifai2.dto.model.output.ClarifaiOutput;
import clarifai2.dto.prediction.Concept;


/**
 * Created by akash on 11/23/2017.
 *
 * Gets an Image
 */

public class ImageRecognizerAsyncTask extends AsyncTask<byte[], Integer, List<List<String>>> {
    private final static String API_KEY = "b8b677d0128049f8a847e200c3469cfb";

    @Override
    protected List<List<String>> doInBackground(byte[]... images) {
        //https://www.javatraineronline.com%2Fjava%2Fimage-recognition-in-java-using-clarifai-api%2F
        // &usg=AOvVaw0FJXHhC_gpOkH76Ys_KCvV
        List<List<String>> totalResultList = new ArrayList<List<String>>();

        for (byte[] image : images) {
            if (image != null) {
                List<String> resultList = new ArrayList<String>();
                final ClarifaiClient client = new ClarifaiBuilder(API_KEY).buildSync();
                final List<ClarifaiOutput<Concept>> predictionResults = client.getDefaultModels()
                        .generalModel().predict().withInputs(ClarifaiInput.forImage(ClarifaiImage
                                .of(image))).executeSync()
                        .get();

                if (predictionResults != null && predictionResults.size() > 0) {
                    for (int i = 0; i < predictionResults.size(); i++) {
                        ClarifaiOutput<Concept> clarifaiOutput = predictionResults.get(i);
                        List<Concept> concepts = clarifaiOutput.data();

                        if (concepts != null && concepts.size() > 0) {
                            for (int j = 0; j < concepts.size(); j++) {
                                resultList.add(concepts.get(j).name());
                            }
                        }
                    }
                }

                totalResultList.add(resultList);
            }
        }

        return totalResultList;
    }
}
