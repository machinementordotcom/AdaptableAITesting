EXIT_STR = 'exit'

def spacer():
    print('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n')

def get_str_choice(i_prompt, *acceptable):
    acceptable = set(acceptable)
    prompt = '\n---------------------------\n'
    prompt += i_prompt + '\n'
    prompt += 'Choices: '

    for acc in acceptable:
        if acc != 'pq':
            prompt += acc + ', '

    prompt += 'or exit'
    prompt += '\nChoice: '

    while True:
        choice = input(prompt)
        spacer()

        for potential in acceptable:
            if potential.startswith(choice) and choice != '':
                return potential

        if choice == EXIT_STR:
            spacer()
            print('Exiting...')
            exit()

        print('Invalid choice %s.' % choice)

def get_int_choice(i_prompt, min_range: int = 0, max_range: int = 10):
    prompt = '\n---------------------------\n'
    prompt += i_prompt + '\n'
    prompt += 'Choices: %i-%i or %s' % (min_range, max_range, EXIT_STR)
    prompt += '\nChoice: '

    while True:   
        choice = input(prompt)
        spacer()
        if choice == EXIT_STR:
            spacer()
            print('Exiting...')
            exit()

        try:
            choice = int(choice)
        except:
            print('Invalid choice. MUST be an integer.')
            continue

        if min_range <= choice <= max_range:
            return choice

        print('\nInvalid choice. Must be between %i and %i' %
              (min_range, max_range))
