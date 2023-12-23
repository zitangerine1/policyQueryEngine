var = [[
    "Google uses your data to provide the services you order and in accordance with the contract terms. They will not use it for any other products or to serve ads. Google's automated systems process your data to provide you services and protection, such as performing spam and malware detection, sorting email, and returning fast search results. They also use your data to track the total number of visitors to the Service, the number of visitors to each page of the Service, and the domain names of your Internet service providers.",
    [['11',
      'Google Cloud Commentary: ○ Google commits to only access or use your data to ... Refer to <b>the Data Usage</b> section of the Google Security whitepaper. Personal&nbsp;...'],
     ['2',
      '... <b>the</b> Service, and <b>the</b> domain names of our visitors&#39; <b>Internet</b> service providers. It is important to note that no Personal <b>Data</b> is available or <b>used</b> in this&nbsp;...'],
     ['9',
      'Know that customer <b>data</b> is not <b>used</b> for advertising. You own <b>your data</b>. Google Cloud does not process <b>your data</b> for advertising purposes. 4. Know where&nbsp;...']]],
    [
        'A data intermediary is an organization that processes personal data on behalf of another organization. Google Cloud is a data intermediary because it processes personal data on behalf of an organization pursuant to a contract for cloud services. Google Cloud commits to only access or use your data to provide the services ordered by you and in accordance with the contract terms.',
        [['5',
          'Topics Key terms &amp; concepts Key term definitions Key concepts <b>Data intermediaries</b> under the PDPA <b>Data intermediary</b> obligations Google Cloud as a data&nbsp;...'],
         ['3',
          'This whitepaper provides information to our customers about Malaysia&#39;s Personal <b>Data</b> Protection Act 2010 (PDPA) and how Google Cloud leverages Google&#39;s industry&nbsp;...'],
         ['10',
          'that we cannot resolve with you directly. European Requirements If European Union (EU) or United Kingdom (UK) <b>data</b> protection law applies to&nbsp;...']]],
    [
        'Google Cloud is a data intermediary under the PDPA because it processes personal data on behalf of an organization pursuant to a contract for cloud services. Google Cloud commits to only access or use your data to provide the services ordered by you and in accordance with the contract terms. ',
        [['6',
          '<b>Google</b> Cloud as a <b>data intermediary Google</b> Cloud qualifies as a <b>data intermediary</b> under the PDPA because it processes personal data on behalf of, or for the&nbsp;...'],
         ['4',
          '<b>Google</b> Cloud 4 At the core of the PDPA are seven Personal <b>Data</b> Protection Principles (Principles) that govern the processing of personal <b>data</b>. Only&nbsp;...'],
         ['10',
          '... <b>data</b> protection authority. For the purposes of EU <b>data</b> protection law, Qwiklabs has appointed <b>Google</b> Cloud EMEA Ltd. as its local representative in the EU&nbsp;...']]]]


def parse_output(sample_output):
    main_texts = []
    nested_arrays = []

    for item in sample_output:
        main_text = item[0]
        nested_array = item[1]

        main_texts.append(main_text)
        nested_arrays.append(nested_array)

        return main_texts, nested_arrays


# Example usage
main_texts, nested_arrays = parse_output(var)

# Print the results
print("Main Texts:")
for text in main_texts:
    print(text)
    print()

print("Nested Arrays:")
for array in nested_arrays:
    print(array)
    print()
