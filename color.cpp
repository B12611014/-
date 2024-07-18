#include <iostream>
#include <opencv2/opencv.hpp>
using namespace std;
using namespace cv;

int main() {
    // 讀取圖片
    //cv::Mat image = cv::imread("path/to/your/image.jpg");
    cv::Mat image = cv::imread("/Users/outingan/C++/project/brown.jpg");  //brown.jpg 是照片檔案 我將他跟這個程式碼存在相同目錄

    // 檢查圖片是否成功讀取
    if (image.empty()) {
        std::cerr << "無法讀取圖片!" << std::endl;
        return -1;
    }

    // 取得圖片的寬和高
    int width = image.cols; 
    int height = image.rows;

    // 顯示圖片的寬和高
    std::cout << "圖片寬度: " << width << std::endl;
    std::cout << "圖片高度: " << height << std::endl;

    int IR[height][width];
    int IG[height][width];
    int IB[height][width];
    
    int blue;
    int green;
    int red;

    // 分析每個像素的 RGB 值
    for (int y = 0; y < height; ++y) {
        for (int x = 0; x < width; ++x) {
            // 取得像素的 RGB 值
            cv::Vec3b pixel = image.at<cv::Vec3b>(y, x);
            blue = pixel[0];
            green = pixel[1];
            red = pixel[2];

            IR[y][x] = red;
            IG[y][x] = green;
            IB[y][x] = blue;

            // 顯示 RGB 值
            //std::cout << "Pixel at (" << x << ", " << y << ") - R: " << red << " G: " << green << " B: " << blue << std::endl;
        }
    }
    // 藉由大便判斷雞是否健康
    int h= 0;    // 大便為棕色 健康
    int w = 0;   // 大便為白色 不健康
    int r = 0;   // 大便為紅色 不健康
    int g = 0;   // 大便為綠色 不健康
    
    //區間範圍是我在網路上利用像素分析軟體取到的數值
    for (int y = 0; y < height; ++y) {
        for (int x = 0; x < width; ++x) {
        
        if(IR[y][x]<=102 && IR[y][x]>=31 && IG[y][x]<=85 && IG[y][x]>=23 && IB[y][x]<=75 && IB[y][x]>=16){
            h++;
        }
        if(IR[y][x]<=266 && IR[y][x]>=161 && IG[y][x]<=244 && IG[y][x]>=177 && IB[y][x]<=255 && IB[y][x]>=202){
            w++;
        }
        if(IR[y][x]<=203 && IR[y][x]>=127 && IG[y][x]<=54 && IG[y][x]>=25 && IB[y][x]<=69 && IB[y][x]>=32){
            r++;
        }
        if(IR[y][x]<=96 && IR[y][x]>=47 && IG[y][x]<=104 && IG[y][x]>=55 && IB[y][x]<=63 && IB[y][x]>=34){
            g++;
        }

        }
    }
    // 顯示圖片
    cv::imshow("Image", image);
    cv::waitKey(0);

    // 我先預設為:如果照片在該區間的像素佔所有像素的60%以上就將此照片分類為該類別
    if(h/width/height >= 0.6){
        cout << "HEALTHY!!!" << endl;
    }
    if(w/width/height >= 0.6){
        cout << "UNHEALTHY!!!" << "white poo-poo " << endl;
    }
    if(r/width/height >= 0.6){
        cout << "UNHEALTHY!!!" << "red poo-poo " <<endl;
    }
    if(g/width/height >= 0.6){
        cout << "UNHEALTHY!!!" << "green poo-poo " << endl;
    }

    return 0;
}

