using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;
using System;
using System.Threading.Tasks;
using Google.Apis.Discovery;
using Google.Apis.Services;
using Google.Apis.Discovery.v1;
using Google.Apis.Discovery.v1.Data;
using System.Net.Http;
using System.Net;
using System.IO;
using System.Text.RegularExpressions;
using InterfaceML.Model;

namespace Interface
{
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
        public MainWindow()
        {
            InitializeComponent();
        }

        private void BtnRetorna_Click(object sender, RoutedEventArgs e)
        {
            Environment.Exit(0);
        }

        private void Window_MouseLeftButtonDown(object sender, MouseButtonEventArgs e)
        {
            if (e.ChangedButton == MouseButton.Left)
                this.DragMove();
        }

        private void Conteudo_MouseEnter(object sender, MouseEventArgs e)
        {
            if (Clipboard.ContainsText(TextDataFormat.Text))
            {
                Conteudo.Text = Clipboard.GetText(TextDataFormat.Text);
            }
        }

        private void Analisar_Click(object sender, RoutedEventArgs e)
        {

            SPConfiabilidade.Visibility = Visibility.Hidden;
            TBConfiabilidade.Text = "";
            Conteudo.Background = Brushes.Transparent;
            bool TemURL = false;
            bool Confiavel = true;
            string HTMLInterno = "";
            if (Conteudo.Text != "")
            {


                foreach (string PrePalavra in Conteudo.Text.Split(" "))
                {

                    if (IsUrlValid(PrePalavra))
                    {
                        TemURL = true;
                        string Palavra = "";
                        if (!PrePalavra.ToUpper().Contains(@"HTTP"))
                        {
                            Palavra = @"http://" + PrePalavra;
                        }
                        else
                        {
                            Palavra = PrePalavra;
                        }

                        HTMLInterno = RetornaHTML(Palavra);
                        if (HTMLInterno != "")
                        {
                            HTMLInterno = HTMLInterno.Split("</title>")[0];

                            HTMLInterno = HTMLInterno.Split("<title>")[1];

                            string frase = HTMLInterno;
                            string key = @"AIzaSyAr-TTl0oCP7p8674s7TZB11xhlKhwxgFY";
                            string Url = @"https://factchecktools.googleapis.com/v1alpha1/claims:search?query=" + frase.Replace(" ", "%20") + "&key=" + key;
                            string Resultado = RetornaHTML(Url);



                            foreach (string Fact in Resultado.Split("\"textualRating\": "))
                            {
                                string Review = Fact.Split("\"languageCode\"")[0];
                                
                                if (Fact.ToLower().Contains("fals") | Fact.ToLower().Contains("fak") | Fact.ToLower().Contains("exa"))
                                {
                                    Confiavel = false;
                                }
                            }
                        }

                    }
                }

                if (!TemURL)
                {
                    // Add input data
                    var input = new ModelInput();

                    input.Tweet = Conteudo.Text;
                    input.Desinf = "";



                    // Load model and predict output of sample data
                    ModelOutput result = ConsumeModel.Predict(input);

                    if (result.Prediction == "desinf")
                    {
                        SPConfiabilidade.Visibility = Visibility.Visible;

                        TBConfiabilidade.Text = Math.Round(result.Score[0], 2) * 100 + " %";
                        Conteudo.Background = Brushes.IndianRed;
                    }
                    else
                    {
                        SPConfiabilidade.Visibility = Visibility.Visible;

                        TBConfiabilidade.Text = Math.Round(result.Score[1], 2) * 100 + " %";
                        Conteudo.Background = Brushes.LightGreen;
                    }

                }


                if (!Confiavel)
                {
                    Conteudo.Background = Brushes.IndianRed;
                }
                else
                {
                    if (HTMLInterno != "")
                    {
                        Conteudo.Background = Brushes.LightGreen;
                    }
                }
            }
           
        }

        private bool IsUrlValid(string url)
        {

            string pattern = @"^(http|https|ftp|)\://|[a-zA-Z0-9\-\.]+\.[a-zA-Z](:[a-zA-Z0-9]*)?/?([a-zA-Z0-9\-\._\?\,\'/\\\+&amp;%\$#\=~])*[^\.\,\)\(\s]$";
            Regex reg = new Regex(pattern, RegexOptions.Compiled | RegexOptions.IgnoreCase);
            return reg.IsMatch(url);
        }

        string RetornaHTML(string URL)
        {
            
                string resultado = "";
                using var client = new HttpClient();

                string urlAddress = URL;
            try
            {
                HttpWebRequest request = (HttpWebRequest)WebRequest.Create(urlAddress);
                HttpWebResponse response = (HttpWebResponse)request.GetResponse();

                if (response.StatusCode == HttpStatusCode.OK)
                {
                    Stream receiveStream = response.GetResponseStream();
                    StreamReader readStream = null;

                    if (String.IsNullOrWhiteSpace(response.CharacterSet))
                        readStream = new StreamReader(receiveStream);
                    else
                        readStream = new StreamReader(receiveStream, Encoding.GetEncoding(response.CharacterSet));

                    resultado = readStream.ReadToEnd();

                    response.Close();
                    readStream.Close();
                }
            }
            catch
            {

            }
            return resultado;
        }



        private async Task Run()
        {
            // Create the service.
            var service = new DiscoveryService(new BaseClientService.Initializer
            {
                BaseUri = @"https://factchecktools.googleapis.com",
                ApplicationName = "Discovery Sample",
                ApiKey = "[YOUR_API_KEY_HERE]",
            }) ;

            // Run the request.
            Console.WriteLine("Executing a list request...");
            var result = await service.Apis.List().ExecuteAsync();

            // Display the results.
            if (result.Items != null)
            {
                foreach (DirectoryList.ItemsData api in result.Items)
                {
                    Console.WriteLine(api.Id + " - " + api.Title);
                }
            }
        }
    }
}
