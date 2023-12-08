const baseURL = 'https://463wvt2kt4.execute-api.us-east-1.amazonaws.com'; 

const APIService = {
    searchPhotos: async (query) => {
        try {
            const response = await fetch(`${baseURL}/search?query=${query}`);
            if (!response.ok) {
              throw new Error('GET Network response was not ok');
            }
            return await response.json();
          } catch (error) {
            throw error;
          }        
    },
    uploadPhoto: async (photo, customLabels) => {
        try {
            const formData = new FormData();
            formData.append('photo', photo);
            formData.append('customLabels', customLabels.join(','));
        
            const response = await fetch(`${baseURL}/*/PUT/upload`, {
              method: 'PUT',
              body: formData,
            });
            if (!response.ok) {
              throw new Error('PUT Network response was not ok');
            }
            return await response.json(); 
          } catch (error) {
            throw error;
          }        
    },
  };  
export default APIService;