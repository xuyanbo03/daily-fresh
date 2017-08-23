import { Pipe, PipeTransform } from '@angular/core';

@Pipe({
  name: 'filter'
})
export class FilterPipe implements PipeTransform {

  transform(people: any, term: any): any {
    if (term === undefined) return people;

    return people.filter((person)=> { return person.name.toLowerCase().includes(term.toLowerCase());});
  }

}
