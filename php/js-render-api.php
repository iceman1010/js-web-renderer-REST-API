<?php
/**
 * PHP Client for js-web-renderer REST API
 */

class JsRenderAPI
{
    public $api_url = 'http://aiworker1.int.opensubtitles.org:9000';
    public $api_key = null;
    public $timeout = 120;

    /**
     * Constructor
     *
     * @param string|null $api_key API key for authentication
     * @param string|null $api_url Base URL for the API
     */
    function __construct($api_key = null, $api_url = null)
    {
        if ($api_key !== null) {
            $this->api_key = $api_key;
        }
        if ($api_url !== null) {
            $this->api_url = rtrim($api_url, '/');
        }
    }

    /**
     * Render a URL and return HTML content
     *
     * @param string $url URL to render
     * @param int $wait Wait time in seconds
     * @param string|null $profile Profile name to use
     * @param array $options Optional parameters (type_actions, click_actions, post_wait, exec_js, post_js)
     * @return array Response data
     */
    function render($url, $wait = 5, $profile = null, $options = [])
    {
        $data = array_merge([
            'url' => $url,
            'wait' => $wait
        ], $options);

        if ($profile !== null) {
            $data['profile'] = $profile;
        }

        return $this->request('POST', '/render', $data);
    }

    /**
     * Take a screenshot of a URL
     *
     * @param string $url URL to screenshot
     * @param int $wait Wait time in seconds
     * @param int $width Viewport width
     * @param int $height Viewport height
     * @param string|null $profile Profile name to use
     * @param array $options Optional parameters (type_actions, click_actions, post_wait, exec_js, post_js)
     * @return string Binary PNG data
     */
    function screenshot($url, $wait = 5, $width = 1280, $height = 900, $profile = null, $options = [])
    {
        $data = array_merge([
            'url' => $url,
            'wait' => $wait,
            'width' => $width,
            'height' => $height
        ], $options);

        if ($profile !== null) {
            $data['profile'] = $profile;
        }

        return $this->request('POST', '/screenshot', $data, true, true);
    }

    /**
     * Get network requests from loading a URL
     *
     * @param string $url URL to analyze
     * @param int $wait Wait time in seconds
     * @param string|null $profile Profile name to use
     * @param array $options Optional parameters (type_actions, click_actions, post_wait, exec_js, post_js)
     * @return array Response data with network requests
     */
    function network($url, $wait = 5, $profile = null, $options = [])
    {
        $data = array_merge([
            'url' => $url,
            'wait' => $wait
        ], $options);

        if ($profile !== null) {
            $data['profile'] = $profile;
        }

        return $this->request('POST', '/network', $data);
    }

    /**
     * List all profiles
     *
     * @return array List of profile names
     */
    function listProfiles()
    {
        return $this->request('GET', '/profiles');
    }

    /**
     * Create a new profile
     *
     * @param string $name Profile name
     * @return array Response data
     */
    function createProfile($name)
    {
        return $this->request('POST', '/profiles', ['name' => $name]);
    }

    /**
     * Get profile information
     *
     * @param string $name Profile name
     * @return array Profile data
     */
    function getProfile($name)
    {
        return $this->request('GET', '/profiles/' . urlencode($name));
    }

    /**
     * Delete a profile
     *
     * @param string $name Profile name
     * @return array Response data
     */
    function deleteProfile($name)
    {
        return $this->request('DELETE', '/profiles/' . urlencode($name));
    }

    /**
     * Check API health status
     *
     * @return array Health status data
     */
    function health()
    {
        return $this->request('GET', '/health', null, false);
    }

    /**
     * Make an HTTP request to the API
     *
     * @param string $method HTTP method (GET, POST, DELETE)
     * @param string $endpoint API endpoint
     * @param array|null $data Request data
     * @param bool $auth Include authorization header
     * @param bool $binary Expect binary response
     * @return array|string Response data or binary content
     * @throws Exception on error
     */
    private function request($method, $endpoint, $data = null, $auth = true, $binary = false)
    {
        $url = $this->api_url . $endpoint;

        $ch = curl_init();
        curl_setopt($ch, CURLOPT_URL, $url);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_TIMEOUT, $this->timeout);

        $headers = [];

        if ($auth && !empty($this->api_key)) {
            $headers[] = 'X-API-Key: ' . $this->api_key;
        }

        if ($method === 'POST') {
            curl_setopt($ch, CURLOPT_POST, true);
            if ($data !== null) {
                $json_data = json_encode($data);
                curl_setopt($ch, CURLOPT_POSTFIELDS, $json_data);
                $headers[] = 'Content-Type: application/json';
            }
        } elseif ($method === 'DELETE') {
            curl_setopt($ch, CURLOPT_CUSTOMREQUEST, 'DELETE');
        }

        if (!empty($headers)) {
            curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);
        }

        $response = curl_exec($ch);
        $http_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
        $error = curl_error($ch);
        curl_close($ch);

        if ($error) {
            throw new Exception("cURL error: $error");
        }

        if ($binary && $http_code === 200) {
            return $response;
        }

        $decoded = json_decode($response, true);

        if ($http_code >= 400) {
            $error_message = isset($decoded['error']) ? $decoded['error'] : "HTTP error $http_code";
            throw new Exception($error_message, $http_code);
        }

        return $decoded;
    }
}
