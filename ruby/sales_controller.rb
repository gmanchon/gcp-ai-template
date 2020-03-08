require 'google/cloud/storage'
require 'google/apis/discovery_v1'
require 'google/apis/ml_v1'

class SalesController < ApplicationController
  def initialize
    # gcp project and bucket
    @project_id = 'le-wagon-data-grupo-bimbo'
    @bucket_name = 'wagon-data-grupo-bimbo-sales'

    # gcp model and version
    @bucket_model_name = 'static_baseline_fixed_resp_4'
    @bucket_model_version = 'v_1'

    # data
    @test_file_name = 'test_10k.csv'
    @test_file_path = "data/#{@test_file_name}"
  end

  def predict
    # download test file
    @downloaded_file_path = download_test_data

    # query discovery
    query_discovery

    # get prediction
    make_prediction
  end

  private

  def download_test_data
    # create storage client
    storage = Google::Cloud::Storage.new project_id: @project_id

    # get file from bucket
    bucket = storage.bucket @bucket_name
    file = bucket.file @test_file_path

    local_path = @test_file_name

    file.download local_path

    file.name
  end

  def query_discovery
    # get discovery client
    service = Google::Apis::DiscoveryV1::DiscoveryService.new

    # list ml api
    @service_discovery = service.list_apis name: 'ml'
  end

  def make_prediction
    # get authorization
    scopes = ['https://www.googleapis.com/auth/cloud-platform']
    authorization = Google::Auth.get_application_default(scopes)

    # create ml engine service
    @ml_service = Google::Apis::MlV1::CloudMachineLearningEngineService.new
    @ml_service.authorization = authorization

    # data
    instances = {
      instances: [
        [1213],
        [1223],
        [1311],
        [1338],
        [1114]
      ]
    }

    # use prediction
    # resource_name = "projects/#{@project_id}/models/#{@bucket_model_name}/"
    resource_name = "projects/#{@project_id}/models/#{@bucket_model_name}/versions/#{@bucket_model_version}/"
    @ml_service.predict_project(
      resource_name,
      instances.to_json, # google_cloud_ml_v1__predict_request_object = nil,
      fields: nil,
      quota_user: nil,
      options: {
        skip_serialization: true,
        skip_deserialization: true
      }
    ) do |result, err|
      @ml_result = result
      @ml_err = err
    end
  end
end
